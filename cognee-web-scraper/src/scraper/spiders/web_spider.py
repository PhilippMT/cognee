"""Scrapy spiders for web crawling."""

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urljoin, urlparse


class WebSpider(CrawlSpider):
    """
    Ethical web crawler that respects robots.txt and follows best practices.
    
    Features:
    - Respects robots.txt automatically (ROBOTSTXT_OBEY=True)
    - Follows links within allowed domains
    - Implements polite crawling with delays
    - Extracts content and images
    """
    
    name = "web_spider"
    
    # Configure via start_requests or settings
    custom_settings = {
        "DEPTH_LIMIT": 3,
        "DOWNLOAD_DELAY": 2,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 4,
    }
    
    def __init__(self, start_urls=None, allowed_domains=None, *args, **kwargs):
        """Initialize spider with dynamic URLs and domains."""
        super().__init__(*args, **kwargs)
        
        # Set start URLs
        if start_urls:
            if isinstance(start_urls, str):
                self.start_urls = [start_urls]
            else:
                self.start_urls = start_urls
        else:
            self.start_urls = []
        
        # Set allowed domains
        if allowed_domains:
            if isinstance(allowed_domains, str):
                self.allowed_domains = [allowed_domains]
            else:
                self.allowed_domains = allowed_domains
        else:
            # Extract domains from start URLs
            self.allowed_domains = [
                urlparse(url).netloc for url in self.start_urls
            ]
        
        # Define crawling rules
        self.rules = (
            Rule(
                LinkExtractor(
                    allow_domains=self.allowed_domains,
                    deny_extensions=[
                        # Binary files
                        'pdf', 'zip', 'tar', 'gz', 'exe', 'dmg', 'pkg',
                        # Media
                        'mp3', 'mp4', 'avi', 'mov', 'wmv', 'flv',
                        # Archives
                        'rar', '7z', 'iso',
                    ],
                ),
                callback="parse_page",
                follow=True,
            ),
        )
        
        # Re-initialize rules after modifying them
        super()._compile_rules()
    
    def parse_page(self, response):
        """
        Parse a web page and extract content.
        
        Extracts:
        - Page title
        - Main content (HTML)
        - Images
        - Links
        - Metadata
        """
        self.logger.info(f"Parsing page: {response.url}")
        
        # Extract basic metadata
        item = {
            "url": response.url,
            "title": response.css("title::text").get(),
            "html": response.text,
            "status": response.status,
            "headers": dict(response.headers),
        }
        
        # Extract images
        image_urls = []
        for img in response.css("img"):
            src = img.css("::attr(src)").get()
            if src:
                # Convert relative URLs to absolute
                abs_url = urljoin(response.url, src)
                image_urls.append(abs_url)
        
        item["image_urls"] = image_urls
        
        # Extract links for reference
        links = []
        for link in response.css("a::attr(href)").getall():
            abs_link = urljoin(response.url, link)
            links.append(abs_link)
        
        item["links"] = links
        
        # Extract meta description
        item["description"] = response.css(
            'meta[name="description"]::attr(content)'
        ).get()
        
        # Extract meta keywords
        item["keywords"] = response.css(
            'meta[name="keywords"]::attr(content)'
        ).get()
        
        # Extract Open Graph data
        item["og_title"] = response.css(
            'meta[property="og:title"]::attr(content)'
        ).get()
        item["og_description"] = response.css(
            'meta[property="og:description"]::attr(content)'
        ).get()
        item["og_image"] = response.css(
            'meta[property="og:image"]::attr(content)'
        ).get()
        
        yield item


class JavaScriptSpider(WebSpider):
    """
    Spider for JavaScript-heavy websites using Playwright.
    
    Renders JavaScript before extracting content.
    """
    
    name = "js_spider"
    
    custom_settings = {
        **WebSpider.custom_settings,
        "PLAYWRIGHT_ENABLED": True,
    }
    
    def start_requests(self):
        """Start requests with Playwright enabled."""
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_goto_kwargs": {
                        "wait_until": "networkidle",
                        "timeout": 30000,
                    },
                },
            )
