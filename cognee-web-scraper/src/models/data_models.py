"""Data models for Cognee knowledge graph."""

from typing import List, Optional
from cognee.low_level import DataPoint


class WebPage(DataPoint):
    """Represent a web page."""
    
    url: str
    title: Optional[str] = None
    description: Optional[str] = None
    content: str  # Markdown content
    keywords: Optional[List[str]] = None
    
    metadata: dict = {
        "index_fields": ["url", "title"]
    }


class Fact(DataPoint):
    """Represent an extracted fact."""
    
    fact: str
    category: Optional[str] = None
    source_url: str
    confidence: float = 1.0
    
    metadata: dict = {
        "index_fields": ["fact", "category", "source_url"]
    }


class Image(DataPoint):
    """Represent an image."""
    
    url: str
    source_page_url: str
    local_path: Optional[str] = None
    alt_text: Optional[str] = None
    
    metadata: dict = {
        "index_fields": ["url", "source_page_url"]
    }


class Website(DataPoint):
    """Represent a website domain."""
    
    domain: str
    pages: List[WebPage]
    
    metadata: dict = {
        "index_fields": ["domain"]
    }
