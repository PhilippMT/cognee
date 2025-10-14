"""Scrapy pipelines for processing scraped data."""

import logging
from pathlib import Path
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter


logger = logging.getLogger(__name__)


class ImageDownloadPipeline(ImagesPipeline):
    """
    Download images from scraped pages.
    
    Features:
    - Downloads images to local storage
    - Deduplicates images using checksums
    - Respects download delays
    - Handles image conversion and thumbnails
    """
    
    def get_media_requests(self, item, info):
        """Generate download requests for images."""
        adapter = ItemAdapter(item)
        image_urls = adapter.get("image_urls", [])
        
        for image_url in image_urls:
            yield scrapy.Request(
                image_url,
                meta={"source_url": adapter["url"]},
            )
    
    def item_completed(self, results, item, info):
        """Process completed downloads."""
        adapter = ItemAdapter(item)
        
        # Store successful downloads
        images = []
        for ok, result in results:
            if ok:
                images.append({
                    "url": result["url"],
                    "path": result["path"],
                    "checksum": result["checksum"],
                })
            else:
                logger.warning(f"Failed to download image: {result}")
        
        adapter["images"] = images
        return item


class ContentProcessingPipeline:
    """
    Process HTML content using ReaderLM-v2.
    
    Converts HTML to clean Markdown and extracts structured data.
    """
    
    def __init__(self):
        """Initialize content processor."""
        from processors.content_processor import ContentProcessor
        self.processor = ContentProcessor()
    
    async def process_item(self, item, spider):
        """Process scraped item."""
        adapter = ItemAdapter(item)
        
        html = adapter.get("html")
        if not html:
            logger.warning(f"No HTML content for {adapter['url']}")
            return item
        
        try:
            # Convert HTML to Markdown
            markdown = await self.processor.html_to_markdown(html)
            adapter["markdown"] = markdown
            
            # Extract structured facts
            facts = await self.processor.extract_facts(markdown, adapter["url"])
            adapter["facts"] = facts
            
            logger.info(f"Processed content from {adapter['url']}")
            
        except Exception as e:
            logger.error(f"Error processing {adapter['url']}: {e}")
            # Don't drop item on processing error
        
        return item


class CogneeIngestionPipeline:
    """
    Ingest processed data into Cognee.
    
    Creates structured data points for knowledge graph ingestion.
    """
    
    def __init__(self):
        """Initialize Cognee ingestion."""
        self.items = []
    
    def process_item(self, item, spider):
        """Collect items for batch ingestion."""
        adapter = ItemAdapter(item)
        
        # Only ingest items with processed content
        if adapter.get("markdown") and adapter.get("facts"):
            self.items.append(dict(adapter))
            logger.info(f"Queued for Cognee ingestion: {adapter['url']}")
        else:
            logger.warning(f"Skipping Cognee ingestion for {adapter['url']} (missing processed content)")
        
        return item
    
    def close_spider(self, spider):
        """Batch ingest all collected items."""
        if not self.items:
            logger.info("No items to ingest into Cognee")
            return
        
        logger.info(f"Ingesting {len(self.items)} items into Cognee")
        
        # Items will be processed by the main pipeline
        # Store for later batch processing
        output_path = Path("data/processed/cognee_items.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        import json
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.items, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(self.items)} items to {output_path}")


# Make scrapy import available
import scrapy
