"""
Episode-Based Temporal Pipeline with Graphiti

This example demonstrates:
- Adding episodes with temporal awareness using Graphiti
- Querying episodes with temporal context
- Building knowledge graphs from episodic data
"""

import os
import asyncio
import pathlib
from datetime import datetime
import cognee
from cognee import config, add, prune
from cognee.shared.logging_utils import setup_logging, INFO


# Sample episodic data with temporal context
episodes_data = [
    {
        "name": "episode_1",
        "text": "Albert Einstein published his theory of special relativity in 1905, fundamentally changing our understanding of space and time.",
        "timestamp": datetime(1905, 6, 30),
        "description": "Special relativity publication"
    },
    {
        "name": "episode_2",
        "text": "In 1915, Einstein completed his general theory of relativity, which described gravity as the curvature of spacetime.",
        "timestamp": datetime(1915, 11, 25),
        "description": "General relativity completion"
    },
    {
        "name": "episode_3",
        "text": "Einstein received the Nobel Prize in Physics in 1921 for his explanation of the photoelectric effect.",
        "timestamp": datetime(1921, 11, 9),
        "description": "Nobel Prize award"
    },
    {
        "name": "episode_4",
        "text": "Einstein emigrated to the United States in 1933 due to the rise of Nazi Germany.",
        "timestamp": datetime(1933, 10, 17),
        "description": "Emigration to USA"
    },
    {
        "name": "episode_5",
        "text": "Einstein passed away on April 18, 1955, in Princeton, New Jersey.",
        "timestamp": datetime(1955, 4, 18),
        "description": "Death"
    }
]


async def main():
    # Set up logging
    logger = setup_logging(log_level=INFO)
    logger.info("Starting episode-based temporal pipeline with Graphiti")

    # Configure data directories
    data_directory_path = str(
        pathlib.Path(os.path.join(pathlib.Path(__file__).parent.parent, ".data_storage")).resolve()
    )
    config.data_root_directory(data_directory_path)

    cognee_directory_path = str(
        pathlib.Path(os.path.join(pathlib.Path(__file__).parent.parent, ".cognee_system")).resolve()
    )
    config.system_root_directory(cognee_directory_path)

    # Clean up previous data for fresh start
    logger.info("Pruning previous data and system metadata")
    await prune.prune_data()
    await prune.prune_system(metadata=True)

    logger.info("\n" + "="*80)
    logger.info("EPISODE-BASED TEMPORAL PROCESSING WITH GRAPHITI")
    logger.info("="*80 + "\n")

    # Method 1: Using Graphiti directly for episode-based processing
    logger.info("--- Method 1: Direct Graphiti Episode Processing ---\n")
    
    try:
        from cognee.tasks.temporal_awareness import build_graph_with_temporal_awareness
        from graphiti_core.nodes import EpisodeType
        
        # Extract text from episodes
        text_list = [ep["text"] for ep in episodes_data]
        
        # Build graph with temporal awareness
        logger.info("Building temporal graph with Graphiti...")
        graphiti = await build_graph_with_temporal_awareness(text_list)
        
        # Add episodes with their temporal metadata
        logger.info("Adding episodes with timestamps...")
        for episode in episodes_data:
            await graphiti.add_episode(
                name=episode["name"],
                episode_body=episode["text"],
                source=EpisodeType.text,
                source_description=episode["description"],
                reference_time=episode["timestamp"],
            )
            logger.info(f"  Added: {episode['name']} ({episode['timestamp'].year})")
        
        # Index graphiti objects for retrieval
        logger.info("\nIndexing Graphiti objects...")
        from cognee.tasks.temporal_awareness.index_graphiti_objects import (
            index_and_transform_graphiti_nodes_and_edges,
        )
        await index_and_transform_graphiti_nodes_and_edges()
        
        # Search for episodes
        logger.info("\n--- Query 1: Search for relativity-related episodes ---")
        from cognee.modules.retrieval.utils.brute_force_triplet_search import (
            brute_force_triplet_search
        )
        
        query1 = "What is relativity?"
        triplets1 = await brute_force_triplet_search(
            query=query1,
            top_k=3,
            collections=["graphitinode_content", "graphitinode_name", "graphitinode_summary"],
        )
        
        logger.info(f"Query: '{query1}'")
        logger.info(f"Found {len(triplets1)} relevant results")
        for i, triplet in enumerate(triplets1[:3], 1):
            source = triplet[0]
            logger.info(f"  Result {i}: {source.get('name', 'unknown')}")
            if 'content' in source:
                logger.info(f"    Content: {source['content'][:100]}...")
        
        logger.info("\n--- Query 2: Search for Nobel Prize information ---")
        query2 = "When did Einstein win the Nobel Prize?"
        triplets2 = await brute_force_triplet_search(
            query=query2,
            top_k=3,
            collections=["graphitinode_content", "graphitinode_name", "graphitinode_summary"],
        )
        
        logger.info(f"Query: '{query2}'")
        logger.info(f"Found {len(triplets2)} relevant results")
        for i, triplet in enumerate(triplets2[:3], 1):
            source = triplet[0]
            logger.info(f"  Result {i}: {source.get('name', 'unknown')}")
            if 'content' in source:
                logger.info(f"    Content: {source['content'][:100]}...")
        
        # Close graphiti connection
        await graphiti.close()
        
        logger.info("\n✓ Episode-based processing with Graphiti completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in Graphiti processing: {e}")
        logger.info("Note: Graphiti requires Neo4j database. Check GRAPH_DATABASE_URL and GRAPH_DATABASE_PASSWORD environment variables.")

    # Method 2: Using episode-based cognify (combines temporal_cognify with Graphiti)
    logger.info("\n" + "="*80)
    logger.info("--- Method 2: Episode-Based Cognify (Hybrid Approach) ---\n")
    
    try:
        # Add episodes to cognee
        texts = [ep["text"] for ep in episodes_data]
        logger.info("Adding episodes to cognee...")
        await add(texts, dataset_name="einstein_episodes")
        
        # Run cognify with temporal awareness
        logger.info("Running temporal cognify...")
        from cognee.api.v1.cognify import cognify
        await cognify(
            datasets=["einstein_episodes"],
            temporal_cognify=True
        )
        
        # Search using temporal search
        logger.info("\n--- Query 3: Temporal search for 1920s events ---")
        from cognee.api.v1.search import search
        from cognee import SearchType
        
        results = await search(
            query_text="What happened in the 1920s?",
            query_type=SearchType.TEMPORAL,
            datasets=["einstein_episodes"],
            top_k=5
        )
        
        logger.info("Temporal search results:")
        if results:
            for result in results:
                logger.info(f"  - {result}")
        else:
            logger.info("  No results found")
        
        logger.info("\n✓ Hybrid episode-based cognify completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in hybrid processing: {e}")

    logger.info("\n" + "="*80)
    logger.info("SUMMARY")
    logger.info("="*80)
    print("\n✓ Demonstrated episode-based temporal processing")
    print("✓ Used Graphiti for temporal graph building")
    print("✓ Added episodes with explicit timestamps")
    print("✓ Performed semantic search across episodes")
    print("✓ Combined with cognee's temporal cognify")
    print("\nKey Capabilities:")
    print("  - Episode-level temporal granularity")
    print("  - Graphiti-based temporal awareness")
    print("  - Semantic similarity search")
    print("  - Time-aware context building")
    print("  - Integration with cognee pipelines")
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
