"""Example: Scrape Documentation Site

This example shows how to scrape a documentation site using the sitemap spider.

Configuration:
- Uses sitemap spider for efficiency
- Scrapes Python documentation
- Stores in separate directory

Best Practices:
1. Use Sitemap - Documentation sites usually have good sitemaps
2. Limit Depth - Set reasonable crawl depth (3-5 levels)
3. Respect Delays - Keep default 2-second delay between requests
4. Monitor Progress - Check logs for crawling status
5. Query Testing - Test queries after ingestion to verify quality
"""

import asyncio
from pathlib import Path
import sys
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pipelines.scrape_website import WebScraperPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


async def main():
    """Scrape a documentation site."""
    
    # Example: Scrape Python documentation
    pipeline = WebScraperPipeline(
        start_urls=[
            "https://docs.python.org/3/tutorial/",
        ],
        allowed_domains=["docs.python.org"],
        use_sitemap=True,
        cognee_dir=".cognee_docs",
        data_dir="data_docs",
    )
    
    await pipeline.run()
    
    # Query the knowledge graph
    result = await pipeline.query("What is Python?")
    print("\nQuery Result:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
