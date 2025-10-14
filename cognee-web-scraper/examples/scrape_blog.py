"""Example: Scrape Blog Posts

This example shows how to scrape blog posts and extract facts.

Tips for Blog Scraping:
1. Use Sitemap - Most blogs have comprehensive sitemaps
2. Extract Facts - Enable fact extraction for blog posts
3. Download Images - Blog images often contain important context
4. Query Topics - Use semantic search to find related posts
5. Time-based Filtering - Consider filtering by publication date
"""

import asyncio
from pathlib import Path
import sys
import logging

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pipelines.scrape_website import WebScraperPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


async def main():
    """Scrape a blog site."""
    
    # Example: Change to your target blog
    pipeline = WebScraperPipeline(
        start_urls=[
            "https://blog.python.org",
        ],
        allowed_domains=["blog.python.org"],
        use_sitemap=True,  # Blogs usually have sitemaps
        cognee_dir=".cognee_blog",
        data_dir="data_blog",
    )
    
    await pipeline.run()
    
    # Example queries
    queries = [
        "What are the main topics covered in the blog?",
        "Summarize the latest posts",
        "What technologies are mentioned?",
    ]
    
    for query in queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        result = await pipeline.query(query)
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
