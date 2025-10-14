"""Main Cognee pipeline for web scraping."""

from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from cognee import config, prune, search, SearchType, visualize_graph
from cognee.low_level import setup
from cognee.pipelines import run_tasks, Task
from cognee.tasks.storage import add_data_points
from cognee.tasks.storage.index_graph_edges import index_graph_edges
from cognee.modules.users.methods import get_default_user
from cognee.modules.data.methods import load_or_create_datasets

import subprocess
import tempfile

# Import our models
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.data_models import WebPage, Fact, Image, Website


logger = logging.getLogger(__name__)


class WebScraperPipeline:
    """
    Complete web scraping pipeline for Cognee.
    
    Steps:
    1. Scrape websites using Scrapy
    2. Process content with ReaderLM-v2
    3. Extract facts and structured data
    4. Ingest into Cognee knowledge graph
    5. Enable search and querying
    """
    
    def __init__(
        self,
        start_urls: List[str],
        allowed_domains: Optional[List[str]] = None,
        use_sitemap: bool = False,
        cognee_dir: str = ".cognee_system",
        data_dir: str = "data",
    ):
        """
        Initialize web scraper pipeline.
        
        Args:
            start_urls: List of URLs to start crawling from
            allowed_domains: Domains allowed for crawling
            use_sitemap: Whether to use sitemap spider
            cognee_dir: Directory for Cognee system files
            data_dir: Directory for downloaded data
        """
        self.start_urls = start_urls
        self.allowed_domains = allowed_domains or [
            urlparse(url).netloc for url in start_urls
        ]
        self.use_sitemap = use_sitemap
        
        # Setup paths
        self.root = Path(__file__).parent.parent.parent
        self.cognee_dir = self.root / cognee_dir
        self.data_dir = self.root / data_dir
        self.artifacts_dir = self.root / ".artifacts"
        
        # Ensure directories exist
        self.cognee_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized WebScraperPipeline for {len(start_urls)} URLs")
    
    def run_scraper(self) -> Path:
        """
        Run Scrapy crawler in a subprocess to avoid event loop conflicts.
        
        Returns:
            Path to scraped data JSON
        """
        logger.info("Starting Scrapy crawler in subprocess...")
        
        output_path = self.data_dir / "processed" / "scraped_data.jsonl"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create a temporary Python script to run Scrapy
        spider_type = "sitemap" if self.use_sitemap else "web"
        src_path = self.root / "src"
        
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
    start_urls={self.start_urls!r},
    allowed_domains={self.allowed_domains!r},
)
process.start()
'''
        
        # Write script to temporary file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(script_content)
            script_path = Path(f.name)
        
        try:
            # Run Scrapy in subprocess
            logger.info(f"Running Scrapy spider: {spider_type}")
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                cwd=str(self.root),
                timeout=3600,  # 1 hour timeout
            )
            
            if result.returncode != 0:
                logger.error(f"Scrapy failed with code {result.returncode}")
                logger.error(f"STDOUT: {result.stdout}")
                logger.error(f"STDERR: {result.stderr}")
                raise RuntimeError(f"Scrapy crawler failed: {result.stderr}")
            
            logger.info("Scraping complete")
            if result.stdout:
                logger.debug(f"Scrapy output: {result.stdout}")
            
        finally:
            # Clean up temporary script
            try:
                script_path.unlink()
            except Exception as e:
                logger.warning(f"Failed to delete temp script: {e}")
        
        if not output_path.exists():
            logger.warning(f"No output file created at {output_path}")
        
        return output_path
    
    def load_scraped_data(self, data_path: Path) -> List[Dict[str, Any]]:
        """Load scraped data from JSONL file."""
        items = []
        
        if not data_path.exists():
            logger.warning(f"No scraped data found at {data_path}")
            return items
        
        with open(data_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    items.append(json.loads(line))
        
        logger.info(f"Loaded {len(items)} scraped items")
        return items
    
    def build_data_nodes(self, items: List[Dict[str, Any]]) -> List[Any]:
        """
        Build Cognee data nodes from scraped items.
        
        Creates:
        - WebPage nodes
        - Fact nodes
        - Image nodes
        - Website nodes with relationships
        """
        # Group by domain
        domains = {}
        all_facts = []
        all_images = []
        
        for item in items:
            url = item.get("url")
            if not url:
                continue
            
            domain = urlparse(url).netloc
            
            # Create WebPage node
            page = WebPage(
                url=url,
                title=item.get("title"),
                description=item.get("description"),
                content=item.get("markdown", ""),
                keywords=item.get("keywords", "").split(",") if item.get("keywords") else None,
            )
            
            # Add to domain
            if domain not in domains:
                domains[domain] = []
            domains[domain].append(page)
            
            # Create Fact nodes
            for fact_data in item.get("facts", []):
                fact = Fact(
                    fact=fact_data.get("fact", ""),
                    category=fact_data.get("category"),
                    source_url=url,
                )
                all_facts.append(fact)
            
            # Create Image nodes
            for image_data in item.get("images", []):
                image = Image(
                    url=image_data.get("url", ""),
                    source_page_url=url,
                    local_path=image_data.get("path"),
                    alt_text=image_data.get("alt"),
                )
                all_images.append(image)
        
        # Create Website nodes
        websites = []
        for domain, pages in domains.items():
            website = Website(
                domain=domain,
                pages=pages,
            )
            websites.append(website)
        
        # Combine all nodes
        all_nodes = websites + all_facts + all_images
        
        logger.info(
            f"Built {len(websites)} websites, "
            f"{sum(len(w.pages) for w in websites)} pages, "
            f"{len(all_facts)} facts, "
            f"{len(all_images)} images"
        )
        
        return all_nodes
    
    async def ingest_to_cognee(self, data_nodes: List[Any]) -> None:
        """
        Ingest data nodes into Cognee.
        
        Args:
            data_nodes: List of data nodes to ingest
        """
        logger.info("Setting up Cognee...")
        
        # Configure Cognee
        config.system_root_directory(str(self.cognee_dir))
        
        # Initialize
        await prune.prune_system(metadata=True)
        await setup()
        
        # Get user and dataset
        user = await get_default_user()
        datasets = await load_or_create_datasets(
            ["web_scraper"], [], user
        )
        dataset_id = datasets[0].id
        
        logger.info(f"Ingesting {len(data_nodes)} nodes into Cognee...")
        
        # Build pipeline
        def provide_data():
            return data_nodes
        
        tasks = [
            Task(provide_data),
            Task(add_data_points),
        ]
        
        pipeline = run_tasks(tasks, dataset_id, None, user, "web_scraper_pipeline")
        
        # Run pipeline
        async for status in pipeline:
            logger.info(f"Pipeline status: {status}")
        
        # Post-process
        logger.info("Indexing graph edges...")
        await index_graph_edges()
        
        # Visualize
        graph_path = self.artifacts_dir / "web_scraper_graph.html"
        logger.info(f"Generating graph visualization at {graph_path}...")
        await visualize_graph(str(graph_path))
        
        logger.info("Cognee ingestion complete!")
    
    async def query(self, query_text: str) -> Any:
        """
        Query the knowledge graph.
        
        Args:
            query_text: Natural language query
            
        Returns:
            Query results
        """
        logger.info(f"Querying: {query_text}")
        
        result = await search(
            query_text=query_text,
            query_type=SearchType.GRAPH_COMPLETION,
        )
        
        return result
    
    async def run(self) -> None:
        """Run the complete pipeline."""
        logger.info("Starting web scraper pipeline...")
        
        # Step 1: Scrape websites
        data_path = self.run_scraper()
        
        # Step 2: Load scraped data
        items = self.load_scraped_data(data_path)
        
        if not items:
            logger.warning("No data scraped. Exiting.")
            return
        
        # Step 3: Build data nodes
        data_nodes = self.build_data_nodes(items)
        
        # Step 4: Ingest to Cognee
        await self.ingest_to_cognee(data_nodes)
        
        # Step 5: Example query
        result = await self.query("What are the main topics covered?")
        logger.info(f"Query result: {result}")
        
        logger.info("Pipeline complete!")


async def main():
    """Main entry point."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    
    # Example usage
    pipeline = WebScraperPipeline(
        start_urls=[
            "https://example.com",
        ],
        use_sitemap=False,  # Set to True to use sitemap
    )
    
    await pipeline.run()


if __name__ == "__main__":
    asyncio.run(main())
