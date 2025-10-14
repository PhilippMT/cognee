"""Test that the subprocess script generation has correct syntax."""

import ast


def test_script_syntax():
    """Verify generated subprocess script has valid Python syntax."""
    
    # Simulate the exact script template from scrape_website.py
    output_path = "/test/output.jsonl"
    spider_type = "web"
    src_path = "/test/src"
    start_urls = ["https://example.com"]
    allowed_domains = ["example.com"]
    
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
    start_urls={start_urls!r},
    allowed_domains={allowed_domains!r},
)
process.start()
'''
    
    # Try to parse the script
    try:
        ast.parse(script_content)
        print("✅ SUCCESS: Generated script has valid Python syntax!")
        print("\nScript validation passed - no indentation errors!")
        print("\nFirst 30 lines of generated script:")
        print("=" * 80)
        for i, line in enumerate(script_content.split('\n')[:30], 1):
            print(f"{i:3d}: {line}")
        print("=" * 80)
        return True
    except SyntaxError as e:
        print("❌ FAILED: Syntax error in generated script!")
        print(f"Error: {e}")
        print(f"Line {e.lineno}: {e.text}")
        print("\nGenerated script:")
        print("=" * 80)
        for i, line in enumerate(script_content.split('\n'), 1):
            marker = " <<<" if i == e.lineno else ""
            print(f"{i:3d}: {line}{marker}")
        print("=" * 80)
        return False


if __name__ == "__main__":
    import sys
    success = test_script_syntax()
    sys.exit(0 if success else 1)
