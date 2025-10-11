"""Example usage of HelixDB Hybrid Adapter

This example demonstrates how to use the HelixDB adapter for hybrid graph-vector operations.

REQUIREMENTS:
- helix-py package installed: pip install helix-py
- HelixDB instance running (local or remote)
- HelixDB schema compiled and deployed

LIMITATIONS:
- This is a demonstration of the adapter interface
- Actual operations require pre-compiled HelixQL queries
- See README.md and ANALYSIS.md for complete limitations
"""

import asyncio
import os
from typing import List

# Import the adapter
from cognee.infrastructure.databases.hybrid.helixdb import HelixDBAdapter

# Import cognee types
from cognee.infrastructure.engine import DataPoint
from cognee.modules.engine.models import Entity, EntityType
from cognee.modules.chunking.models import DocumentChunk
from cognee.modules.data.processing.document_types import TextDocument

# Import embedding engine
from cognee.infrastructure.databases.vector.embeddings import get_embedding_engine
from cognee.shared.logging_utils import get_logger

logger = get_logger("helixdb_example")


async def example_vector_operations():
    """Example: Vector operations with HelixDB adapter"""
    logger.info("=== Vector Operations Example ===")
    
    # Initialize adapter
    embedding_engine = get_embedding_engine()
    adapter = HelixDBAdapter(
        config_path=os.getenv("HELIX_CONFIG_PATH", "./helixdb-cfg"),
        port=6969,
        local=True,
        embedding_engine=embedding_engine,
        auto_start=False  # Assume instance already running
    )
    
    # Create collection
    collection_name = "example_documents"
    await adapter.create_collection(collection_name)
    logger.info(f"Created collection: {collection_name}")
    
    # Create some documents
    class ExampleDocument(DataPoint):
        text: str
        category: str
        metadata: dict = {"index_fields": ["text"]}
    
    documents = [
        ExampleDocument(
            id="doc1",
            text="HelixDB is a graph-vector database built in Rust",
            category="technology"
        ),
        ExampleDocument(
            id="doc2",
            text="Vector search enables semantic similarity matching",
            category="ai"
        ),
        ExampleDocument(
            id="doc3",
            text="Graph databases model relationships between entities",
            category="databases"
        ),
    ]
    
    # Insert documents with embeddings
    logger.info(f"Inserting {len(documents)} documents...")
    await adapter.create_data_points(collection_name, documents)
    
    # Search by text (vector similarity)
    logger.info("Performing vector search...")
    search_results = await adapter.search(
        collection_name=collection_name,
        query_text="database for semantic search",
        limit=2
    )
    logger.info(f"Found {len(search_results)} results")
    
    # Retrieve specific documents
    logger.info("Retrieving specific documents...")
    retrieved = await adapter.retrieve(
        collection_name=collection_name,
        data_point_ids=["doc1", "doc2"]
    )
    logger.info(f"Retrieved {len(retrieved)} documents")
    
    logger.info("✓ Vector operations example complete")
    logger.warning("Note: Actual operations require pre-compiled HelixQL queries")


async def example_graph_operations():
    """Example: Graph operations with HelixDB adapter"""
    logger.info("=== Graph Operations Example ===")
    
    # Initialize adapter (no embedding engine needed for graph-only operations)
    adapter = HelixDBAdapter(
        config_path=os.getenv("HELIX_CONFIG_PATH", "./helixdb-cfg"),
        port=6969,
        local=True,
        embedding_engine=None,
        auto_start=False
    )
    
    # Create entities
    python_entity = Entity(
        name="Python",
        description="High-level programming language"
    )
    
    rust_entity = Entity(
        name="Rust",
        description="Systems programming language"
    )
    
    helixdb_entity = Entity(
        name="HelixDB",
        description="Graph-vector database"
    )
    
    # Add nodes to graph
    logger.info("Adding nodes to graph...")
    await adapter.add_nodes([python_entity, rust_entity, helixdb_entity])
    
    # Add relationships
    logger.info("Adding edges...")
    await adapter.add_edge(
        source_id=str(rust_entity.id),
        target_id=str(helixdb_entity.id),
        relationship_name="IMPLEMENTED_IN",
        properties={"since": "2024"}
    )
    
    await adapter.add_edge(
        source_id=str(python_entity.id),
        target_id=str(helixdb_entity.id),
        relationship_name="HAS_SDK",
        properties={"package": "helix-py"}
    )
    
    # Query nodes
    logger.info(f"Querying node: {python_entity.id}")
    node = await adapter.get_node(str(python_entity.id))
    
    # Get neighbors
    logger.info("Getting neighbors...")
    neighbors = await adapter.get_neighbors(str(helixdb_entity.id))
    logger.info(f"Found {len(neighbors)} neighbors")
    
    # Get all connections
    logger.info("Getting connections...")
    connections = await adapter.get_connections(str(helixdb_entity.id))
    logger.info(f"Found {len(connections)} connections")
    
    logger.info("✓ Graph operations example complete")
    logger.warning("Note: Actual operations require pre-compiled HelixQL queries")


async def example_hybrid_operations():
    """Example: Combined graph and vector operations"""
    logger.info("=== Hybrid Operations Example ===")
    
    # Initialize adapter with embedding engine
    embedding_engine = get_embedding_engine()
    adapter = HelixDBAdapter(
        config_path=os.getenv("HELIX_CONFIG_PATH", "./helixdb-cfg"),
        port=6969,
        local=True,
        embedding_engine=embedding_engine,
        auto_start=False
    )
    
    # Create a document
    document = TextDocument(
        name="python_guide.txt",
        raw_data_location="examples/python_guide.txt",
        external_metadata="{}",
        mime_type="text/plain"
    )
    
    # Create chunks
    chunk1 = DocumentChunk(
        text="Python is a high-level programming language that emphasizes code readability",
        chunk_size=75,
        chunk_index=0,
        cut_type="sentence_end",
        is_part_of=document
    )
    
    chunk2 = DocumentChunk(
        text="Python supports multiple programming paradigms including procedural and object-oriented",
        chunk_size=88,
        chunk_index=1,
        cut_type="sentence_end",
        is_part_of=document
    )
    
    # Add document and chunks as graph nodes
    logger.info("Adding document and chunks as graph nodes...")
    await adapter.add_nodes([document, chunk1, chunk2])
    
    # Add relationships
    logger.info("Adding relationships...")
    await adapter.add_edge(
        source_id=str(chunk1.id),
        target_id=str(document.id),
        relationship_name="IS_PART_OF"
    )
    
    await adapter.add_edge(
        source_id=str(chunk2.id),
        target_id=str(document.id),
        relationship_name="IS_PART_OF"
    )
    
    # Also add chunks to vector index for semantic search
    logger.info("Adding chunks to vector index...")
    await adapter.create_data_points("document_chunks", [chunk1, chunk2])
    
    # Now we can:
    # 1. Use graph traversal to find related chunks
    logger.info("Traversing graph relationships...")
    edges = await adapter.get_edges(str(chunk1.id))
    logger.info(f"Found {len(edges)} edges for chunk1")
    
    # 2. Use vector search to find semantically similar chunks
    logger.info("Performing semantic search...")
    similar_chunks = await adapter.search(
        collection_name="document_chunks",
        query_text="programming language features",
        limit=5
    )
    logger.info(f"Found {len(similar_chunks)} similar chunks")
    
    logger.info("✓ Hybrid operations example complete")
    logger.warning("Note: Actual operations require pre-compiled HelixQL queries")


async def example_custom_query():
    """Example: Using custom HelixQL queries"""
    logger.info("=== Custom Query Example ===")
    
    adapter = HelixDBAdapter(
        config_path=os.getenv("HELIX_CONFIG_PATH", "./helixdb-cfg"),
        port=6969,
        local=True,
        auto_start=False
    )
    
    # Execute a custom pre-compiled query
    # This assumes you have defined this query in your .hx files:
    # 
    # QUERY findEntitiesByType(entity_type: String) =>
    #     entities <- N<Entity::WHERE(_::{type}::EQ(entity_type))>
    #     RETURN entities
    #
    logger.info("Executing custom query...")
    try:
        results = await adapter.query(
            "findEntitiesByType",
            {"entity_type": "programming_language"}
        )
        logger.info(f"Query returned {len(results)} results")
    except Exception as e:
        logger.error(f"Query failed (expected if not compiled): {e}")
    
    logger.info("✓ Custom query example complete")
    logger.warning("Note: Query must be pre-compiled in .hx files and deployed")


async def main():
    """Run all examples"""
    logger.info("Starting HelixDB Adapter Examples")
    logger.info("=" * 60)
    
    try:
        await example_vector_operations()
        print()
        
        await example_graph_operations()
        print()
        
        await example_hybrid_operations()
        print()
        
        await example_custom_query()
        print()
        
        logger.info("=" * 60)
        logger.info("All examples completed!")
        logger.info("")
        logger.info("IMPORTANT NOTES:")
        logger.info("1. This adapter is a stub implementation")
        logger.info("2. Actual operations require pre-compiled HelixQL queries")
        logger.info("3. See README.md for setup instructions")
        logger.info("4. See ANALYSIS.md for complete limitations")
        logger.info("")
        logger.info("To use this adapter in production:")
        logger.info("- Define schema in .hx files")
        logger.info("- Compile queries with 'helix check'")
        logger.info("- Deploy with 'helix deploy'")
        logger.info("- Implement actual query calls in adapter methods")
        
    except Exception as e:
        logger.error(f"Example failed: {e}")
        raise


if __name__ == "__main__":
    # Run examples
    asyncio.run(main())
