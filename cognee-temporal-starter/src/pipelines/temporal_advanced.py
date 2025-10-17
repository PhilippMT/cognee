"""
Advanced Temporal Pipeline Example

This example demonstrates:
- Processing multiple documents with temporal information
- Complex temporal queries
- Event relationship tracking
- Visualization of temporal graphs
"""

import os
import asyncio
import pathlib
import cognee
from cognee import config, add, prune, SearchType, visualize_graph
from cognee.api.v1.cognify import cognify
from cognee.api.v1.search import search
from cognee.shared.logging_utils import setup_logging, INFO
from cognee.infrastructure.databases.graph import get_graph_engine


# Sample historical data with multiple interconnected events
world_war_data = """
World War II began on September 1, 1939, when Germany invaded Poland. Two days later, 
on September 3, 1939, Britain and France declared war on Germany. The United States 
initially remained neutral but provided aid to the Allies through the Lend-Lease Act, 
which was passed on March 11, 1941.

The war expanded to the Pacific when Japan attacked Pearl Harbor on December 7, 1941. 
This prompted the United States to officially enter the war on December 8, 1941. 
The Battle of Midway, fought from June 4-7, 1942, marked a turning point in the Pacific theater.

In Europe, the D-Day invasion occurred on June 6, 1944, when Allied forces landed in Normandy, 
France. The Battle of the Bulge, from December 16, 1944 to January 25, 1945, was Germany's 
last major offensive on the Western Front.

Germany surrendered on May 8, 1945, known as V-E Day (Victory in Europe Day). The atomic 
bombs were dropped on Hiroshima on August 6, 1945, and Nagasaki on August 9, 1945. 
Japan formally surrendered on September 2, 1945, marking V-J Day and the end of World War II.
"""

tech_revolution_data = """
The digital revolution accelerated rapidly in the 1990s. The World Wide Web was made 
publicly available on August 6, 1991, by Tim Berners-Lee at CERN. The first web browser, 
Mosaic, was released on April 22, 1993, making the internet accessible to the general public.

Amazon was founded by Jeff Bezos on July 5, 1994, initially as an online bookstore. 
Google was incorporated on September 4, 1998, by Larry Page and Sergey Brin while they 
were Ph.D. students at Stanford University.

The dot-com bubble reached its peak on March 10, 2000, before crashing later that year. 
Wikipedia was launched on January 15, 2001, by Jimmy Wales and Larry Sanger. 
Facebook was founded on February 4, 2004, by Mark Zuckerberg while he was a student at Harvard.

The first iPhone was announced by Steve Jobs on January 9, 2007, and released on June 29, 2007, 
revolutionizing mobile computing. The advent of cloud computing became mainstream around 2008-2010, 
with major services like AWS, Azure, and Google Cloud gaining widespread adoption.
"""


async def main():
    # Set up logging
    logger = setup_logging(log_level=INFO)
    logger.info("Starting advanced temporal pipeline example")

    # Configure directories
    data_directory_path = str(
        pathlib.Path(os.path.join(pathlib.Path(__file__).parent.parent, ".data_storage")).resolve()
    )
    config.data_root_directory(data_directory_path)

    cognee_directory_path = str(
        pathlib.Path(os.path.join(pathlib.Path(__file__).parent.parent, ".cognee_system")).resolve()
    )
    config.system_root_directory(cognee_directory_path)

    # Clean up for fresh start
    logger.info("Pruning previous data")
    await prune.prune_data()
    await prune.prune_system(metadata=True)

    # Add multiple datasets with temporal information
    logger.info("Adding World War II historical data")
    await add([world_war_data], dataset_name="wwii_history")

    logger.info("Adding tech revolution data")
    await add([tech_revolution_data], dataset_name="tech_history")

    # Run temporal cognify on both datasets
    logger.info("Running temporal cognify on all datasets")
    await cognify(
        datasets=["wwii_history", "tech_history"],
        temporal_cognify=True
    )

    logger.info("\n" + "="*80)
    logger.info("ADVANCED TEMPORAL QUERIES")
    logger.info("="*80 + "\n")

    # Query 1: WWII events in a specific year range
    logger.info("\n--- Query 1: WWII events 1939-1941 ---")
    results_1 = await search(
        query_text="What major events happened between 1939 and 1941?",
        query_type=SearchType.TEMPORAL,
        datasets=["wwii_history"],
        top_k=10
    )
    logger.info(f"Results: {results_1}\n")

    # Query 2: Tech events in the 1990s
    logger.info("\n--- Query 2: Technology events in the 1990s ---")
    results_2 = await search(
        query_text="What technological developments occurred in the 1990s?",
        query_type=SearchType.TEMPORAL,
        datasets=["tech_history"],
        top_k=10
    )
    logger.info(f"Results: {results_2}\n")

    # Query 3: Specific event - Pearl Harbor
    logger.info("\n--- Query 3: Pearl Harbor attack ---")
    results_3 = await search(
        query_text="When was Pearl Harbor attacked?",
        query_type=SearchType.TEMPORAL,
        datasets=["wwii_history"],
        top_k=5
    )
    logger.info(f"Results: {results_3}\n")

    # Query 4: Tech company foundings
    logger.info("\n--- Query 4: Major tech company foundings ---")
    results_4 = await search(
        query_text="When were major tech companies like Google and Amazon founded?",
        query_type=SearchType.TEMPORAL,
        datasets=["tech_history"],
        top_k=10
    )
    logger.info(f"Results: {results_4}\n")

    # Query 5: Cross-dataset temporal query
    logger.info("\n--- Query 5: Events in the 2000s (both datasets) ---")
    results_5 = await search(
        query_text="What happened between 2000 and 2010?",
        query_type=SearchType.TEMPORAL,
        datasets=["wwii_history", "tech_history"],
        top_k=10
    )
    logger.info(f"Results: {results_5}\n")

    # Query 6: Specific date range - D-Day period
    logger.info("\n--- Query 6: Events around D-Day (June 1944) ---")
    results_6 = await search(
        query_text="What happened in June 1944?",
        query_type=SearchType.TEMPORAL,
        datasets=["wwii_history"],
        top_k=5
    )
    logger.info(f"Results: {results_6}\n")

    # Get graph statistics
    logger.info("\n--- Graph Statistics ---")
    try:
        graph_engine = await get_graph_engine()
        graph = await graph_engine.get_graph_data()
        
        from collections import Counter
        node_type_counts = Counter(node_data[1].get("type", {}) for node_data in graph[0])
        edge_type_counts = Counter(edge_type[2] for edge_type in graph[1])
        
        logger.info(f"Node counts by type: {dict(node_type_counts)}")
        logger.info(f"Edge counts by type: {dict(edge_type_counts)}")
        logger.info(f"Total nodes: {len(graph[0])}")
        logger.info(f"Total edges: {len(graph[1])}")
        logger.info(f"Event nodes: {node_type_counts.get('Event', 0)}")
        logger.info(f"Timestamp nodes: {node_type_counts.get('Timestamp', 0)}")
    except Exception as e:
        logger.warning(f"Could not retrieve graph statistics: {e}")

    # Visualize the graph
    logger.info("\n--- Creating Graph Visualization ---")
    try:
        artifacts_dir = pathlib.Path(os.path.join(pathlib.Path(__file__).parent.parent, ".artifacts"))
        artifacts_dir.mkdir(exist_ok=True)
        
        graph_file_path = str(artifacts_dir / "temporal_graph_visualization.html")
        await visualize_graph(graph_file_path)
        logger.info(f"Graph visualization saved to: {graph_file_path}")
    except Exception as e:
        logger.warning(f"Could not create visualization: {e}")

    logger.info("\n" + "="*80)
    logger.info("SUMMARY")
    logger.info("="*80)
    print("\n✓ Processed multiple datasets with temporal information")
    print("✓ Extracted events and timestamps from historical and tech data")
    print("✓ Performed complex temporal queries across time ranges")
    print("✓ Demonstrated cross-dataset temporal search")
    print("✓ Generated graph statistics and visualization")
    print("\nKey Capabilities Demonstrated:")
    print("  - Multi-dataset temporal processing")
    print("  - Year/decade-based queries")
    print("  - Specific date range filtering")
    print("  - Event relationship tracking")
    print("  - Temporal graph analysis")
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
