"""
Standalone Scrapy runner for testing.

This script runs Scrapy independently to test the crawler without
the full Cognee pipeline.

Usage:
    python src/run_scraper_standalone.py
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from scrapy.crawler import CrawlerProcess
from scraper import settings as scraper_settings


def main():
    """Run Scrapy crawler standalone."""
    
    # Create settings dict
    settings_dict = {
        name: getattr(scraper_settings, name)
        for name in dir(scraper_settings)
        if name.isupper() and not name.startswith('_')
    }
    
    # Override settings for testing (use FEEDS instead of deprecated FEED_URI/FEED_FORMAT)
    settings_dict["FEEDS"] = {
        "data/processed/test_scraped_data.jsonl": {
            "format": "jsonlines",
            "encoding": "utf-8",
            "store_empty": False,
            "overwrite": True,
        }
    }
    settings_dict["LOG_LEVEL"] = "INFO"
    settings_dict["CLOSESPIDER_PAGECOUNT"] = 5  # Limit for testing
    
    # Create crawler
    process = CrawlerProcess(settings_dict)
    
    # Use WebSpider
    from scraper.spiders.web_spider import WebSpider
    
    # Configure spider
    process.crawl(
        WebSpider,
        start_urls=["https://example.com"],
        allowed_domains=["example.com"],
    )
    
    # Start crawling
    print("Starting Scrapy crawler...")
    process.start()
    print("Scraping complete!")


if __name__ == "__main__":
    main()
