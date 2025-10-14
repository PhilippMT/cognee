"""Scrapy settings for web scraper."""

BOT_NAME = "cognee-web-scraper"

SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

# Crawl responsibly by identifying yourself
USER_AGENT = "CogneeBot/1.0 (+https://github.com/topoteretes/cognee)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 4

# Configure delays for requests
DOWNLOAD_DELAY = 2  # 2 seconds between requests
RANDOMIZE_DOWNLOAD_DELAY = True  # Random delay 0.5x - 1.5x

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
}

# Enable or disable spider middlewares
SPIDER_MIDDLEWARES = {
    "scrapy.spidermiddlewares.httperror.HttpErrorMiddleware": 50,
    "scrapy.spidermiddlewares.referer.RefererMiddleware": 700,
    "scrapy.spidermiddlewares.urllength.UrlLengthMiddleware": 800,
    "scrapy.spidermiddlewares.depth.DepthMiddleware": 900,
}

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware": 100,
    "scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware": 300,
    "scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware": 350,
    "scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware": 400,
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": 500,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 550,
    "scrapy.downloadermiddlewares.redirect.RedirectMiddleware": 600,
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 590,
}

# Enable or disable extensions
EXTENSIONS = {
    "scrapy.extensions.telnet.TelnetConsole": None,
    "scrapy.extensions.logstats.LogStats": 500,
}

# Configure item pipelines
ITEM_PIPELINES = {
    "scraper.pipelines.ImageDownloadPipeline": 1,
    "scraper.pipelines.ContentProcessingPipeline": 300,
    "scraper.pipelines.CogneeIngestionPipeline": 800,
}

# Images Pipeline Settings
IMAGES_STORE = "data/downloads/images"
IMAGES_URLS_FIELD = "image_urls"
IMAGES_RESULT_FIELD = "images"
IMAGES_EXPIRES = 90  # Days

# Files Pipeline Settings
FILES_STORE = "data/downloads/files"
FILES_URLS_FIELD = "file_urls"
FILES_RESULT_FIELD = "files"

# Enable and configure HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400  # 24 hours
HTTPCACHE_DIR = "data/.httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 408, 429]
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Crawl depth
DEPTH_LIMIT = 3
DEPTH_PRIORITY = 1

# Download timeout
DOWNLOAD_TIMEOUT = 30

# Retry settings
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# AutoThrottle settings
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
AUTOTHROTTLE_DEBUG = False

# Log settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
LOG_DATEFORMAT = "%Y-%m-%d %H:%M:%S"

# Stats
STATS_DUMP = True

# Memory usage
MEMUSAGE_ENABLED = True
MEMUSAGE_LIMIT_MB = 2048
MEMUSAGE_WARNING_MB = 1024

# Feed exports
FEEDS = {
    "data/processed/scraped_data.jsonl": {
        "format": "jsonlines",
        "encoding": "utf-8",
        "store_empty": False,
        "overwrite": True,
    }
}

# Playwright settings (for JavaScript-heavy sites)
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "timeout": 30000,
}

# Custom settings
CUSTOM_SETTINGS = {
    "CLOSESPIDER_PAGECOUNT": 1000,  # Stop after 1000 pages
    "CLOSESPIDER_TIMEOUT": 3600,  # Stop after 1 hour
}
