# Changelog

All notable changes to the Cognee Web Scraper project.

## [1.1.0] - 2025-10-10

### Fixed
- **RuntimeError: Event loop conflict** - Implemented subprocess-based Scrapy execution to isolate Twisted reactor from asyncio event loop
- **Deprecated FEED_URI/FEED_FORMAT** - Replaced with modern `FEEDS` dictionary configuration (Scrapy 2.1+)
- **Deprecated offsite spider middleware** - Removed `scrapy.spidermiddlewares.offsite.OffsiteMiddleware` (now handled by downloader middleware)
- **Settings import** - Changed from `get_project_settings()` to direct module import for better reliability

### Changed
- All feed export configurations now use `FEEDS` dictionary format
- Spider middleware configuration no longer includes deprecated offsite middleware
- Scrapy execution runs in isolated subprocess to prevent event loop conflicts

### Added
- Standalone test script `src/run_scraper_standalone.py` for independent testing
- Comprehensive troubleshooting section in README.md
- Detailed fixes documentation in FIXES_APPLIED.md
- Windows compatibility notes for vLLM limitations

### Tested
- ✅ No deprecation warnings in Scrapy 2.13.3
- ✅ No event loop errors during execution
- ✅ All pipelines load correctly
- ✅ robots.txt middleware functioning
- ✅ HTTP caching operational

---

## [1.0.0] - 2025-10-10

### Added
- Initial project structure and implementation
- Web scraping with Scrapy (WebSpider, SitemapSpider, JavaScriptSpider)
- robots.txt and sitemap.xml support
- Image download pipeline with deduplication
- ReaderLM-v2 integration for HTML→Markdown conversion
- Fact extraction using LLM
- Cognee data models (WebPage, Fact, Image, Website)
- Main pipeline orchestrator
- Comprehensive documentation (README, QUICKSTART, IMPLEMENTATION)
- Multiple usage examples

### Features
- Polite crawling with configurable delays
- Auto-throttling based on server response
- HTTP caching for efficiency
- Playwright support for JavaScript-rendered sites
- OpenAI-compatible API integration for content processing
- Knowledge graph ingestion with Cognee

---

## Notes

### Platform Compatibility
- **Windows**: Scrapy works fully, vLLM requires WSL2/Linux
- **Linux/macOS**: Full support including vLLM with GPU acceleration

### Dependencies
- Scrapy >= 2.12.0
- Cognee >= 0.1.38
- vLLM >= 0.8.3 (optional, Linux/macOS only)
- Playwright >= 1.49.0
- Python >= 3.12

---

**Maintained by**: Cognee Team  
**Repository**: [GitHub](https://github.com/topoteretes/cognee)
