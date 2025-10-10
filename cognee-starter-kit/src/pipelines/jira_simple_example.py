"""
Simple example of Jira ticket ingestion pipeline.

This script demonstrates:
1. Parsing Jira tickets from XML
2. Creating a knowledge graph with ontology
3. Querying tickets with graph search
4. Temporal awareness for ticket changes

Run with: python src/pipelines/jira_simple_example.py
"""

import asyncio
import logging
import os
from pathlib import Path

import cognee
from cognee.api.v1.search import SearchType
from cognee.modules.ontology.rdf_xml.RDFLibOntologyResolver import RDFLibOntologyResolver
from cognee.modules.ontology.ontology_config import Config

from ..parsers.jira_xml_parser import parse_jira_xml


# Paths
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT.parent / "data"
JIRA_XML = DATA_DIR / "jira_tickets.xml"
JIRA_ONTOLOGY = DATA_DIR / "jira_ontology.owl"


async def main():
    """Run simple Jira ticket ingestion example."""
    
    logging.basicConfig(level=logging.INFO)
    print("\n" + "="*70)
    print("Jira Ticket Ingestion Example")
    print("="*70 + "\n")
    
    # Step 1: Parse Jira tickets
    print("Step 1: Parsing Jira tickets from XML...")
    tickets = parse_jira_xml(JIRA_XML)
    print(f"✓ Parsed {len(tickets)} tickets\n")
    
    # Display parsed tickets
    for ticket in tickets:
        print(f"  • {ticket.ticket_id}: {ticket.summary}")
        print(f"    Status: {ticket.status.name} | Priority: {ticket.priority.name}")
        print(f"    Changes: {len(ticket.history)} history records")
        print()
    
    # Step 2: Reset and prepare cognee
    print("Step 2: Preparing knowledge graph...")
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    print("✓ System reset complete\n")
    
    # Step 3: Convert tickets to text for ingestion
    # For simple example, we'll create text descriptions
    print("Step 3: Converting tickets to text format...")
    ticket_texts = []
    for ticket in tickets:
        text = f"""
Jira Ticket: {ticket.ticket_id}
Summary: {ticket.summary}
Description: {ticket.description}
Status: {ticket.status.name}
Priority: {ticket.priority.name}
Type: {ticket.ticket_type.name}
Reporter: {ticket.reporter.email}
Assignee: {ticket.assignee.email if ticket.assignee else "Unassigned"}
Created: {ticket.created_date}
Updated: {ticket.updated_date}
Components: {", ".join([c.name for c in ticket.components])}
Labels: {", ".join([l.name for l in ticket.labels])}

History:
"""
        for change in ticket.history:
            text += f"- {change.timestamp}: {change.field} changed from '{change.from_value}' to '{change.to_value}' by {change.author.email}\n"
        
        ticket_texts.append(text)
    
    print(f"✓ Converted {len(ticket_texts)} tickets to text\n")
    
    # Step 4: Add tickets to cognee
    print("Step 4: Adding tickets to Cognee...")
    await cognee.add(ticket_texts)
    print("✓ Tickets added\n")
    
    # Step 5: Run cognify with ontology
    print("Step 5: Building knowledge graph with Jira ontology...")
    if JIRA_ONTOLOGY.exists():
        ontology_config: Config = {
            "ontology_config": {
                "ontology_resolver": RDFLibOntologyResolver(ontology_file=str(JIRA_ONTOLOGY))
            }
        }
        await cognee.cognify(config=ontology_config, temporal_cognify=True)
        print("✓ Knowledge graph created with ontology and temporal awareness\n")
    else:
        await cognee.cognify(temporal_cognify=True)
        print("✓ Knowledge graph created with temporal awareness\n")
    
    # Step 6: Run example queries
    print("Step 6: Running example queries...")
    print("-" * 70 + "\n")
    
    queries = [
        ("What tickets are currently in progress?", SearchType.GRAPH_COMPLETION),
        ("Show me all critical priority tickets", SearchType.GRAPH_COMPLETION),
        ("What security-related tickets exist?", SearchType.GRAPH_COMPLETION),
        ("Tell me about PROJ-123", SearchType.GRAPH_COMPLETION),
    ]
    
    for query_text, query_type in queries:
        print(f"Query: {query_text}")
        print(f"Type: {query_type.name}")
        
        try:
            results = await cognee.search(
                query_text=query_text,
                query_type=query_type,
                top_k=3
            )
            print(f"Results:\n{results}\n")
        except Exception as e:
            print(f"Error: {e}\n")
        
        print("-" * 70 + "\n")
    
    # Step 7: Show ticket statistics
    print("Step 7: Ticket Statistics")
    print("-" * 70)
    
    status_counts = {}
    priority_counts = {}
    type_counts = {}
    
    for ticket in tickets:
        status_counts[ticket.status.name] = status_counts.get(ticket.status.name, 0) + 1
        priority_counts[ticket.priority.name] = priority_counts.get(ticket.priority.name, 0) + 1
        type_counts[ticket.ticket_type.name] = type_counts.get(ticket.ticket_type.name, 0) + 1
    
    print("\nStatus Distribution:")
    for status, count in status_counts.items():
        print(f"  {status}: {count}")
    
    print("\nPriority Distribution:")
    for priority, count in priority_counts.items():
        print(f"  {priority}: {count}")
    
    print("\nType Distribution:")
    for ticket_type, count in type_counts.items():
        print(f"  {ticket_type}: {count}")
    
    print("\n" + "="*70)
    print("Example Complete!")
    print("="*70 + "\n")
    
    print("Next steps:")
    print("  1. Modify jira_tickets.xml to add your own tickets")
    print("  2. Run this script again to ingest the updated data")
    print("  3. Check out jira_pipeline.py for advanced features like versioning")
    print("  4. See JIRA_PIPELINE_README.md for full documentation")


if __name__ == "__main__":
    asyncio.run(main())
