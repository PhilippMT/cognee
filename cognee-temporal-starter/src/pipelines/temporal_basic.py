"""
Basic Temporal Pipeline Example

This example demonstrates:
- Adding text data with temporal information
- Running cognify with temporal awareness enabled
- Performing temporal search queries
- Extracting events within specific time ranges
"""

import os
import asyncio
import pathlib
import cognee
from cognee import config, add, prune, SearchType
from cognee.api.v1.cognify import cognify
from cognee.api.v1.search import search
from cognee.shared.logging_utils import setup_logging, INFO

# Sample biographical data with temporal events
biography_data = """
Marie Curie was born on November 7, 1867, in Warsaw, Poland. In 1891, she moved to Paris 
to study physics and mathematics at the Sorbonne. In 1903, she became the first woman to 
win a Nobel Prize, sharing the Physics prize with her husband Pierre Curie and Henri Becquerel 
for their work on radioactivity. After Pierre's death in 1906, she took over his teaching 
position at the Sorbonne, becoming the first female professor there.

In 1911, Marie Curie won her second Nobel Prize, this time in Chemistry, for her discovery 
of radium and polonium. During World War I (1914-1918), she developed mobile X-ray units 
to help wounded soldiers. She continued her research throughout the 1920s and early 1930s, 
until her death on July 4, 1934, from aplastic anemia caused by radiation exposure.
"""


async def main():
    # Set up logging
    logger = setup_logging(log_level=INFO)
    logger.info("Starting temporal pipeline example")

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

    # Add biographical data
    logger.info("Adding biographical data")
    await add([biography_data], dataset_name="marie_curie_biography")

    # Run cognify with temporal awareness enabled
    logger.info("Running temporal cognify - extracting events and timestamps")
    await cognify(
        datasets=["marie_curie_biography"],
        temporal_cognify=True
    )

    logger.info("\n" + "="*80)
    logger.info("Temporal cognify completed! Now running queries...")
    logger.info("="*80 + "\n")

    # Query 1: General temporal search
    logger.info("\n--- Query 1: Events in early 1900s ---")
    results_1 = await search(
        query_text="What happened between 1900 and 1910?",
        query_type=SearchType.TEMPORAL,
        datasets=["marie_curie_biography"],
        top_k=5
    )
    logger.info(f"Results: {results_1}\n")

    # Query 2: Specific event search
    logger.info("\n--- Query 2: Nobel Prize events ---")
    results_2 = await search(
        query_text="When did Marie Curie win Nobel Prizes?",
        query_type=SearchType.TEMPORAL,
        datasets=["marie_curie_biography"],
        top_k=5
    )
    logger.info(f"Results: {results_2}\n")

    # Query 3: WWI period
    logger.info("\n--- Query 3: World War I period activities ---")
    results_3 = await search(
        query_text="What did she do during World War I?",
        query_type=SearchType.TEMPORAL,
        datasets=["marie_curie_biography"],
        top_k=5
    )
    logger.info(f"Results: {results_3}\n")

    # Query 4: Early life
    logger.info("\n--- Query 4: Early life events ---")
    results_4 = await search(
        query_text="What happened in Marie Curie's early life before 1900?",
        query_type=SearchType.TEMPORAL,
        datasets=["marie_curie_biography"],
        top_k=5
    )
    logger.info(f"Results: {results_4}\n")

    logger.info("\n" + "="*80)
    logger.info("Temporal pipeline example completed successfully!")
    logger.info("="*80 + "\n")

    # Print summary
    print("\n" + "="*80)
    print("SUMMARY: Temporal Graph Features Demonstrated")
    print("="*80)
    print("✓ Temporal event extraction from biographical text")
    print("✓ Timestamp identification and parsing")
    print("✓ Time-range based query filtering")
    print("✓ Event retrieval with temporal context")
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
