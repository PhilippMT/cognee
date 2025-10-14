"""Configuration for web scraper."""

from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ScraperConfig:
    """Configuration for web scraping."""
    
    # Target URLs
    start_urls: List[str]
    allowed_domains: Optional[List[str]] = None
    
    # Crawling behavior
    use_sitemap: bool = False
    crawl_depth: int = 3
    max_pages: int = 1000
    
    # Politeness
    download_delay: float = 2.0
    concurrent_requests: int = 8
    randomize_delay: bool = True
    
    # Content processing
    extract_images: bool = True
    extract_facts: bool = True
    max_facts_per_page: int = 20
    
    # ReaderLM-v2 settings
    vllm_api_base: str = "http://localhost:8000/v1"
    vllm_model: str = "jinaai/ReaderLM-v2"
    max_context_length: int = 32768
    
    # Storage
    data_dir: str = "data"
    cognee_dir: str = ".cognee_system"
    artifacts_dir: str = ".artifacts"
    
    # Logging
    log_level: str = "INFO"


# Default configuration
DEFAULT_CONFIG = ScraperConfig(
    start_urls=["https://example.com"],
    crawl_depth=2,
    max_pages=100,
)


# Example configurations
DOCUMENTATION_CONFIG = ScraperConfig(
    start_urls=["https://docs.example.com"],
    use_sitemap=True,
    crawl_depth=5,
    max_pages=500,
    download_delay=1.0,
)

NEWS_CONFIG = ScraperConfig(
    start_urls=["https://news.example.com"],
    use_sitemap=True,
    crawl_depth=2,
    max_pages=1000,
    extract_facts=True,
    max_facts_per_page=30,
)

BLOG_CONFIG = ScraperConfig(
    start_urls=["https://blog.example.com"],
    use_sitemap=True,
    crawl_depth=3,
    extract_images=True,
    extract_facts=True,
)
