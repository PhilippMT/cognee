"""
Cognee pipeline for Jira ticket ingestion with temporal awareness.

This pipeline demonstrates two versioning strategies:
1. UPDATE_LATEST: Overwrite existing tickets by ticket_id (keep only latest version)
2. STORE_ALL_VERSIONS: Store all versions with version tracking (retrieve latest on query)

The pipeline includes:
- XML parsing of Jira tickets
- Temporal awareness for ticket changes
- Ontology-based knowledge graph construction
- Graph-based search and querying
"""

from __future__ import annotations

import asyncio
import logging
import os
from enum import Enum
from pathlib import Path
from typing import Any, List, Optional
from collections import defaultdict

from cognee import config, prune, search, SearchType, visualize_graph
from cognee.low_level import setup, DataPoint
from cognee.pipelines import run_tasks, Task
from cognee.tasks.storage import add_data_points
from cognee.tasks.storage.index_graph_edges import index_graph_edges
from cognee.modules.users.methods import get_default_user
from cognee.modules.data.methods import load_or_create_datasets
from cognee.modules.ontology.rdf_xml.RDFLibOntologyResolver import RDFLibOntologyResolver
from cognee.modules.ontology.ontology_config import Config

from ..parsers.jira_xml_parser import parse_jira_xml
from ..models.jira_models import JiraTicket


class VersioningStrategy(Enum):
    """Strategy for handling ticket updates."""
    UPDATE_LATEST = "update_latest"  # Overwrite existing tickets
    STORE_ALL_VERSIONS = "store_all_versions"  # Keep all versions


# Configuration
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT.parent / "data"
COGNEE_DIR = ROOT / ".cognee_jira"
ARTIFACTS_DIR = ROOT / ".artifacts"
GRAPH_HTML = ARTIFACTS_DIR / "jira_graph_visualization.html"
JIRA_XML = DATA_DIR / "jira_tickets.xml"
JIRA_ONTOLOGY = DATA_DIR / "jira_ontology.owl"

# Global state for versioning
_ticket_versions: dict[str, List[JiraTicket]] = defaultdict(list)
_versioning_strategy: VersioningStrategy = VersioningStrategy.UPDATE_LATEST


def set_versioning_strategy(strategy: VersioningStrategy):
    """Set the versioning strategy for ticket ingestion."""
    global _versioning_strategy
    _versioning_strategy = strategy
    logging.info(f"Versioning strategy set to: {strategy.value}")


def ingest_jira_tickets(xml_path: str | Path | None = None) -> List[JiraTicket]:
    """
    Ingest Jira tickets from XML file.
    
    Handles versioning based on configured strategy:
    - UPDATE_LATEST: Returns only the latest version of each ticket
    - STORE_ALL_VERSIONS: Returns all versions with version numbers
    
    Args:
        xml_path: Path to XML file (defaults to JIRA_XML)
        
    Returns:
        List of JiraTicket objects ready for storage
    """
    if xml_path is None:
        xml_path = JIRA_XML
    
    logging.info(f"Parsing Jira tickets from {xml_path}")
    tickets = parse_jira_xml(xml_path)
    logging.info(f"Parsed {len(tickets)} tickets")
    
    global _ticket_versions, _versioning_strategy
    
    if _versioning_strategy == VersioningStrategy.UPDATE_LATEST:
        # Simple case: just return latest tickets (overwrite on re-ingest)
        for ticket in tickets:
            _ticket_versions[ticket.ticket_id] = [ticket]
        return tickets
    
    elif _versioning_strategy == VersioningStrategy.STORE_ALL_VERSIONS:
        # Store all versions with version tracking
        result_tickets = []
        for ticket in tickets:
            ticket_id = ticket.ticket_id
            existing_versions = _ticket_versions[ticket_id]
            
            # Check if this exact version already exists (by updated_date)
            existing = next(
                (t for t in existing_versions if t.updated_date == ticket.updated_date),
                None
            )
            
            if existing is None:
                # New version - assign version number
                version_num = len(existing_versions) + 1
                ticket.version = version_num
                _ticket_versions[ticket_id].append(ticket)
                result_tickets.append(ticket)
                logging.info(f"Added new version {version_num} for ticket {ticket_id}")
            else:
                # Already have this version
                logging.info(f"Ticket {ticket_id} version already exists, skipping")
                result_tickets.append(existing)
        
        return result_tickets
    
    return tickets


def get_latest_ticket_version(ticket_id: str) -> Optional[JiraTicket]:
    """
    Retrieve the latest version of a ticket by ticket_id.
    
    This is useful when querying for a specific ticket and you want
    the most recent state.
    """
    versions = _ticket_versions.get(ticket_id, [])
    if not versions:
        return None
    
    # Return ticket with highest version number or latest updated_date
    return max(versions, key=lambda t: (t.version, t.updated_date))


def get_all_ticket_versions(ticket_id: str) -> List[JiraTicket]:
    """
    Retrieve all versions of a ticket by ticket_id.
    
    Useful for temporal analysis of how a ticket changed over time.
    """
    return _ticket_versions.get(ticket_id, [])


async def execute_jira_pipeline(
    xml_path: str | Path | None = None,
    use_ontology: bool = True,
    versioning: VersioningStrategy = VersioningStrategy.UPDATE_LATEST
) -> None:
    """
    Execute the Jira ticket ingestion pipeline.
    
    Args:
        xml_path: Path to Jira XML file (defaults to example data)
        use_ontology: Whether to use Jira ontology for knowledge graph
        versioning: Strategy for handling ticket versions
    """
    # Set versioning strategy
    set_versioning_strategy(versioning)
    
    # Configure system paths
    logging.info(f"Configuring Cognee directories at {COGNEE_DIR}")
    config.system_root_directory(str(COGNEE_DIR))
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Reset state and initialize
    await prune.prune_system(metadata=True)
    await setup()
    
    # Get user and dataset
    user = await get_default_user()
    datasets = await load_or_create_datasets(["jira_tickets"], [], user)
    dataset_id = datasets[0].id
    
    # Build and run pipeline with custom ingestion
    tasks = [
        Task(lambda data=None: ingest_jira_tickets(xml_path)),
        Task(add_data_points)
    ]
    pipeline = run_tasks(tasks, dataset_id, None, user, "jira_pipeline")
    
    logging.info("Running Jira ingestion pipeline...")
    async for status in pipeline:
        logging.info(f"Pipeline status: {status}")
    
    # Post-process: index graph edges
    await index_graph_edges()
    
    # Run cognify with optional ontology
    if use_ontology and JIRA_ONTOLOGY.exists():
        logging.info(f"Using Jira ontology from {JIRA_ONTOLOGY}")
        import cognee
        ontology_config: Config = {
            "ontology_config": {
                "ontology_resolver": RDFLibOntologyResolver(ontology_file=str(JIRA_ONTOLOGY))
            }
        }
        await cognee.cognify(config=ontology_config, temporal_cognify=True)
        logging.info("Knowledge graph created with Jira ontology and temporal awareness")
    else:
        logging.info("Creating knowledge graph without ontology")
        import cognee
        await cognee.cognify(temporal_cognify=True)
    
    # Visualize graph
    await visualize_graph(str(GRAPH_HTML))
    logging.info(f"Graph visualization saved to {GRAPH_HTML}")
    
    # Example queries
    await run_example_queries()


async def run_example_queries():
    """Run example queries to demonstrate the system."""
    logging.info("\n" + "="*60)
    logging.info("Running example queries...")
    logging.info("="*60 + "\n")
    
    queries = [
        {
            "text": "What tickets are currently in progress?",
            "type": SearchType.GRAPH_COMPLETION
        },
        {
            "text": "Show me all critical priority tickets",
            "type": SearchType.GRAPH_COMPLETION
        },
        {
            "text": "What tickets were created in February 2024?",
            "type": SearchType.TEMPORAL
        },
        {
            "text": "Show me the history of PROJ-123",
            "type": SearchType.GRAPH_COMPLETION
        },
        {
            "text": "What security-related tickets exist?",
            "type": SearchType.GRAPH_COMPLETION
        },
    ]
    
    for query_info in queries:
        query_text = query_info["text"]
        query_type = query_info["type"]
        
        logging.info(f"\nQuery: {query_text}")
        logging.info(f"Type: {query_type}")
        
        try:
            results = await search(
                query_text=query_text,
                query_type=query_type,
                top_k=5
            )
            logging.info(f"Results: {results}\n")
        except Exception as e:
            logging.error(f"Query failed: {e}\n")


def configure_logging() -> None:
    """Configure logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


async def main() -> None:
    """Run main function."""
    configure_logging()
    
    logging.info("\n" + "="*60)
    logging.info("Jira Ticket Ingestion Pipeline")
    logging.info("="*60 + "\n")
    
    # Demonstrate both versioning strategies
    logging.info("Strategy 1: UPDATE_LATEST (overwrite existing tickets)")
    logging.info("-" * 60)
    try:
        await execute_jira_pipeline(
            versioning=VersioningStrategy.UPDATE_LATEST,
            use_ontology=True
        )
    except Exception as e:
        logging.exception("Pipeline failed with UPDATE_LATEST strategy")
        raise
    
    logging.info("\n\n" + "="*60)
    logging.info("Strategy 2: STORE_ALL_VERSIONS (keep version history)")
    logging.info("-" * 60)
    
    # Clean up for second run
    global _ticket_versions
    _ticket_versions.clear()
    
    try:
        await execute_jira_pipeline(
            versioning=VersioningStrategy.STORE_ALL_VERSIONS,
            use_ontology=True
        )
        
        # Demonstrate version retrieval
        logging.info("\n" + "="*60)
        logging.info("Demonstrating version retrieval:")
        logging.info("="*60)
        
        latest = get_latest_ticket_version("PROJ-123")
        if latest:
            logging.info(f"\nLatest version of PROJ-123:")
            logging.info(f"  Version: {latest.version}")
            logging.info(f"  Status: {latest.status.name}")
            logging.info(f"  Updated: {latest.updated_date}")
            logging.info(f"  History changes: {len(latest.history)}")
        
        all_versions = get_all_ticket_versions("PROJ-123")
        logging.info(f"\nAll versions of PROJ-123: {len(all_versions)} total")
        for ticket in all_versions:
            logging.info(f"  Version {ticket.version}: {ticket.status.name} (updated: {ticket.updated_date})")
        
    except Exception as e:
        logging.exception("Pipeline failed with STORE_ALL_VERSIONS strategy")
        raise


if __name__ == "__main__":
    asyncio.run(main())
