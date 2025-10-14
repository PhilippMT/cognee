"""Sitemap spider for efficient crawling."""

import scrapy
from scrapy.spiders import SitemapSpider as BaseSpider
from urllib.parse import urljoin


class SitemapSpider(BaseSpider):
    """
    Efficient crawler using sitemap.xml.
    
    Features:
    - Automatically discovers and follows sitemap.xml
    - Follows sitemap indices
    - Respects robots.txt sitemap directives
    - More efficient than recursive crawling for large sites
    """
    
    name = "sitemap_spider"
    
    def __init__(self, start_urls=None, allowed_domains=None, *args, **kwargs):
        """Initialize sitemap spider."""
        super().__init__(*args, **kwargs)
        
        # Set sitemap URLs (typically <domain>/sitemap.xml)
        if start_urls:
            if isinstance(start_urls, str):
                urls = [start_urls]
            else:
                urls = start_urls
            
            # Convert to sitemap URLs
            self.sitemap_urls = []
            for url in urls:
                # Try both /sitemap.xml and /sitemap_index.xml
                if not url.endswith("sitemap.xml") and not url.endswith("sitemap_index.xml"):
                    self.sitemap_urls.append(urljoin(url, "/sitemap.xml"))
                    self.sitemap_urls.append(urljoin(url, "/sitemap_index.xml"))
                else:
                    self.sitemap_urls.append(url)
        
        # Set allowed domains
        if allowed_domains:
            if isinstance(allowed_domains, str):
                self.allowed_domains = [allowed_domains]
            else:
                self.allowed_domains = allowed_domains
    
    # Rules for filtering URLs
    sitemap_rules = [
        # Include all URLs by default
        (r".*", "parse_page"),
    ]
    
    # Follow sitemap indices
    sitemap_follow = [".*"]
    
    # Include alternate language links
    sitemap_alternate_links = True
    
    def parse_page(self, response):
        """
        Parse a page discovered from sitemap.
        
        Similar to WebSpider.parse_page but optimized for sitemap crawling.
        """
        self.logger.info(f"Parsing sitemap URL: {response.url}")
        
        item = {
            "url": response.url,
            "title": response.css("title::text").get(),
            "html": response.text,
            "status": response.status,
        }
        
        # Extract images
        image_urls = []
        for img in response.css("img"):
            src = img.css("::attr(src)").get()
            if src:
                abs_url = urljoin(response.url, src)
                image_urls.append(abs_url)
        
        item["image_urls"] = image_urls
        
        # Extract metadata
        item["description"] = response.css(
            'meta[name="description"]::attr(content)'
        ).get()
        
        # Extract lastmod from sitemap if available
        lastmod = response.xpath(
            '//lastmod/text()'
        ).get()
        if lastmod:
            item["lastmod"] = lastmod
        
        # Extract priority from sitemap if available
        priority = response.xpath(
            '//priority/text()'
        ).get()
        if priority:
            item["priority"] = float(priority)
        
        yield item
    
    def sitemap_filter(self, entries):
        """
        Filter sitemap entries.
        
        Can be overridden to implement custom filtering logic.
        """
        for entry in entries:
            # Filter by date, priority, etc.
            # For now, include all entries
            yield entry
