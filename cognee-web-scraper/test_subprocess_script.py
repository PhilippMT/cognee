"""Test that the subprocess script generation has correct syntax."""

import ast
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pipelines.scrape_website import WebScraperPipeline


def test_script_syntax():
    """Verify generated subprocess script has valid Python syntax."""
    
    pipeline = WebScraperPipeline(
        start_urls=["https://example.com"],
        allowed_domains=["example.com"],
    )
    
    # Generate the script content (extract from run_scraper method)
    output_path = Path("test_output.jsonl")
    spider_type = "web"
    src_path = Path(__file__).parent / "src"
    
    script_content = f'''"""Scrapy subprocess runner."""
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, r"{src_path}")

from scrapy.crawler import CrawlerProcess
from scrapy import signals

# Import settings module directly
from scraper import settings as scraper_settings

# Create settings dict
settings_dict = {{
    name: getattr(scraper_settings, name)
    for name in dir(scraper_settings)
    if name.isupper() and not name.startswith('_')
}}

# Override feed settings (use FEEDS instead of deprecated FEED_URI/FEED_FORMAT)
settings_dict["FEEDS"] = {{
    r"{output_path}": {{
        "format": "jsonlines",
        "encoding": "utf-8",
        "store_empty": False,
        "overwrite": True,
    }}
}}
settings_dict["LOG_LEVEL"] = "INFO"

# Create crawler
process = CrawlerProcess(settings_dict)

# Choose and configure spider
if "{spider_type}" == "sitemap":
    from scraper.spiders.sitemap_spider import SitemapSpider
    spider_cls = SitemapSpider
else:
    from scraper.spiders.web_spider import WebSpider
    spider_cls = WebSpider

# Start crawling
process.crawl(
    spider_cls,
    start_urls={pipeline.start_urls!r},
    allowed_domains={pipeline.allowed_domains!r},
)
process.start()
'''
    
    # Try to parse the script
    try:
        ast.parse(script_content)
        print("✅ SUCCESS: Generated script has valid Python syntax!")
        print("\nGenerated script:")
        print("=" * 80)
        print(script_content)
        print("=" * 80)
        return True
    except SyntaxError as e:
        print(f"❌ FAILED: Syntax error in generated script!")
        print(f"Error: {e}")
        print(f"Line {e.lineno}: {e.text}")
        print("\nGenerated script:")
        print("=" * 80)
        print(script_content)
        print("=" * 80)
        return False


if __name__ == "__main__":
    success = test_script_syntax()
    sys.exit(0 if success else 1)
