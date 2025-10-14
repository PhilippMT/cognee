"""Web scraper package."""

__version__ = "0.1.0"

from .pipelines.scrape_website import WebScraperPipeline
from .config.scraper_config import ScraperConfig

__all__ = [
    "WebScraperPipeline",
    "ScraperConfig",
]
