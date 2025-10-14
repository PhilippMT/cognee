"""
Simple example: Scrape a single webpage

This minimal example demonstrates the core functionality:
1. Scrape a single URL
2. Process with ReaderLM-v2
3. Ingest into Cognee
4. Query the knowledge graph

Usage:
    python examples/simple_example.py
"""

import asyncio
import logging
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pipelines.scrape_website import WebScraperPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


async def main():
    """Run simple scraping example."""
    
    logger.info("Starting simple web scraper example...")
    
    # Create pipeline with minimal configuration
    # Change this URL to any website you want to scrape
    pipeline = WebScraperPipeline(
        start_urls=[
            "https://example.com",  # Change to your target
        ],
        use_sitemap=False,  # Simple crawling, no sitemap
    )
    
    # Run the complete pipeline
    logger.info("Running scraper pipeline...")
    await pipeline.run()
    
    logger.info("Pipeline complete! Check:")
    logger.info("  - data/processed/scraped_data.jsonl for raw data")
    logger.info("  - data/downloads/images/ for images")
    logger.info("  - .artifacts/web_scraper_graph.html for visualization")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise
