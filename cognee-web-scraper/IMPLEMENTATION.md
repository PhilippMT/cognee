# Cognee Web Scraper - Implementation Summary

## Project Overview

A complete web scraping and crawling pipeline for Cognee that:
- ✅ Uses Scrapy for ethical web crawling
- ✅ Respects robots.txt and sitemap.xml
- ✅ Downloads websites and images
- ✅ Uses Jina ReaderLM-v2 for HTML→Markdown conversion
- ✅ Extracts facts using local LLM
- ✅ Ingests data into Cognee knowledge graph
- ✅ Enables semantic search and querying

## Architecture

```
┌─────────────┐
│  Start URLs │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│   Scrapy Spider                 │
│   - Respects robots.txt         │
│   - Follows sitemap.xml         │
│   - Polite crawling (delays)    │
│   - Downloads HTML & images     │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   Content Processing            │
│   - ReaderLM-v2 (HTML→Markdown) │
│   - Fact extraction (LLM)       │
│   - Image processing            │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   Cognee Ingestion              │
│   - WebPage nodes               │
│   - Fact nodes                  │
│   - Image nodes                 │
│   - Knowledge graph building    │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   Query & Visualization         │
│   - Semantic search             │
│   - Graph queries               │
│   - Visualization               │
└─────────────────────────────────┘
```

## Project Structure

```
cognee-web-scraper/
├── src/
│   ├── scraper/
│   │   ├── spiders/
│   │   │   ├── web_spider.py          # Main crawler
│   │   │   └── sitemap_spider.py      # Sitemap-based crawler
│   │   ├── pipelines.py               # Scrapy processing pipelines
│   │   └── settings.py                # Scrapy configuration
│   ├── processors/
│   │   └── content_processor.py       # ReaderLM-v2 integration
│   ├── models/
│   │   └── data_models.py             # Cognee data models
│   ├── config/
│   │   └── scraper_config.py          # Configuration classes
│   └── pipelines/
│       └── scrape_website.py          # Main Cognee pipeline
├── examples/
│   ├── scrape_docs.py                 # Documentation scraping example
│   └── scrape_blog.py                 # Blog scraping example
├── data/                              # Data storage (gitignored)
├── pyproject.toml                     # Dependencies
├── scrapy.cfg                         # Scrapy project config
├── .env.template                      # Environment variables template
├── .gitignore
├── README.md                          # Full documentation
└── QUICKSTART.md                      # Quick start guide
```

## Key Components

### 1. Scrapy Spiders

#### WebSpider (`src/scraper/spiders/web_spider.py`)
- Recursive crawling within allowed domains
- Respects robots.txt automatically
- Implements polite delays (2 seconds default)
- Extracts HTML, images, links, metadata
- Supports JavaScript rendering via Playwright

#### SitemapSpider (`src/scraper/spiders/sitemap_spider.py`)
- Efficient crawling using sitemap.xml
- Follows sitemap indices
- Automatically discovers sitemaps from robots.txt
- Better for large, well-structured sites

### 2. Content Processing

#### ContentProcessor (`src/processors/content_processor.py`)
- **HTML Cleaning**: Removes scripts, styles, comments, base64 images
- **HTML→Markdown**: Uses ReaderLM-v2 via vLLM OpenAI-compatible API
- **Fact Extraction**: Uses LLM to extract structured facts
- **Structured Data**: Can extract custom JSON schemas

Key features:
- Local inference with vLLM
- OpenAI-compatible API
- Supports up to 512K token context
- Multi-language support (29 languages)

### 3. Scrapy Pipelines

#### ImageDownloadPipeline (`src/scraper/pipelines.py`)
- Downloads images to local storage
- Deduplicates using checksums
- Converts and resizes images

#### ContentProcessingPipeline
- Processes HTML with ReaderLM-v2
- Extracts facts from content
- Handles errors gracefully

#### CogneeIngestionPipeline
- Collects processed items
- Batches for Cognee ingestion
- Saves to JSON for later processing

### 4. Cognee Integration

#### Data Models (`src/models/data_models.py`)
- **WebPage**: URL, title, content (Markdown), metadata
- **Fact**: Extracted fact, category, source
- **Image**: URL, source page, local path
- **Website**: Domain with related pages

#### Pipeline (`src/pipelines/scrape_website.py`)
- **WebScraperPipeline**: Main orchestrator
  - Runs Scrapy crawler
  - Loads scraped data
  - Builds Cognee data nodes
  - Ingests into knowledge graph
  - Enables querying and visualization

### 5. Configuration

#### Scraper Settings (`src/scraper/settings.py`)
Comprehensive Scrapy settings:
- `ROBOTSTXT_OBEY = True` - Respects robots.txt
- `DOWNLOAD_DELAY = 2` - Polite 2-second delay
- `DEPTH_LIMIT = 3` - Max crawl depth
- `CONCURRENT_REQUESTS = 8` - Parallel requests
- HTTP caching enabled
- Auto-throttle enabled
- Image/file pipelines configured

#### ScraperConfig (`src/config/scraper_config.py`)
Python configuration classes:
- DEFAULT_CONFIG
- DOCUMENTATION_CONFIG
- NEWS_CONFIG
- BLOG_CONFIG

## Setup Instructions

### 1. Install Dependencies

```bash
# Install Python dependencies
uv sync

# Install Playwright browsers
playwright install chromium
```

### 2. Start ReaderLM-v2 Server

```bash
# Start vLLM server
vllm serve jinaai/ReaderLM-v2 \
  --dtype auto \
  --api-key token-abc123 \
  --max-model-len 32768 \
  --port 8000
```

**Requirements**:
- GPU with 8GB+ VRAM (RTX 3090/4090 recommended)
- CUDA 11.8+
- 16GB+ system RAM

### 3. Configure Environment

```bash
# Copy template
cp .env.template .env

# Edit .env with your API keys
nano .env
```

Required variables:
- `VLLM_API_BASE` - vLLM server URL
- `LLM_PROVIDER` - LLM provider for Cognee
- `LLM_API_KEY` - API key
- `EMBEDDING_PROVIDER` - Embedding provider
- `EMBEDDING_API_KEY` - Embedding API key

## Usage Examples

### Example 1: Scrape Documentation

```python
from pipelines.scrape_website import WebScraperPipeline
import asyncio

async def main():
    pipeline = WebScraperPipeline(
        start_urls=["https://docs.python.org/3/"],
        allowed_domains=["docs.python.org"],
        use_sitemap=True,
    )
    
    await pipeline.run()
    
    result = await pipeline.query("What is Python?")
    print(result)

asyncio.run(main())
```

### Example 2: Scrape Blog

```python
pipeline = WebScraperPipeline(
    start_urls=["https://blog.example.com"],
    use_sitemap=True,
)
await pipeline.run()
```

### Example 3: Custom Configuration

```python
from config.scraper_config import ScraperConfig

config = ScraperConfig(
    start_urls=["https://example.com"],
    crawl_depth=5,
    max_pages=500,
    download_delay=1.0,
    extract_facts=True,
)
```

## Best Practices Implemented

### Ethical Crawling
1. ✅ **Respects robots.txt** - Automatic via Scrapy
2. ✅ **Follows sitemap.xml** - Sitemap spider implementation
3. ✅ **Polite delays** - 2-second default, randomized
4. ✅ **Descriptive User-Agent** - Identifies as CogneeBot
5. ✅ **Rate limiting** - Auto-throttle enabled
6. ✅ **Depth limits** - Prevents excessive crawling
7. ✅ **Concurrent request limits** - Avoids overloading servers

### Content Processing
1. ✅ **HTML cleaning** - Removes noise (scripts, styles, comments)
2. ✅ **Deduplication** - HTTP cache and image checksums
3. ✅ **Error handling** - Graceful failure recovery
4. ✅ **Batch processing** - Efficient for large sites
5. ✅ **Context preservation** - Maintains semantic information

### Performance
1. ✅ **HTTP caching** - 24-hour cache
2. ✅ **Parallel requests** - Configurable concurrency
3. ✅ **Image deduplication** - Checksum-based
4. ✅ **Memory monitoring** - Auto-throttle and limits
5. ✅ **Incremental processing** - Pipeline-based

## Technology Stack

### Core
- **Scrapy 2.12+** - Web crawling framework
- **Cognee 0.1.38+** - Knowledge graph ingestion
- **Jina ReaderLM-v2** - HTML→Markdown conversion
- **vLLM 0.8.3+** - LLM inference server

### Additional
- **Playwright** - JavaScript rendering
- **Pillow** - Image processing
- **OpenAI** - API client for vLLM
- **Transformers** - Model loading
- **Protego** - robots.txt parsing

## Data Flow

1. **Scraping Phase**
   - Spider discovers URLs (links or sitemap)
   - Downloads HTML and images
   - Respects robots.txt and delays
   - Saves to JSONL file

2. **Processing Phase**
   - Cleans HTML (remove scripts, styles)
   - Converts to Markdown (ReaderLM-v2)
   - Extracts facts (LLM)
   - Processes images

3. **Ingestion Phase**
   - Builds Cognee data nodes
   - Creates relationships
   - Adds to knowledge graph
   - Indexes for search

4. **Query Phase**
   - Semantic search
   - Graph traversal
   - LLM-powered completion

## Limitations & Future Enhancements

### Current Limitations
- Single-threaded Scrapy (Twisted reactor)
- vLLM requires GPU
- No distributed crawling
- No JavaScript rendering by default

### Future Enhancements
1. **Distributed Crawling** - Scrapy Cloud or custom
2. **JavaScript Support** - Enable Playwright by default
3. **Better Deduplication** - Content-based hashing
4. **Incremental Updates** - Only scrape new/changed pages
5. **Advanced Filtering** - URL patterns, date ranges
6. **Multi-modal** - Better image understanding
7. **Monitoring** - Dashboard and metrics

## Testing

Run the example scripts:

```bash
# Documentation example
python examples/scrape_docs.py

# Blog example  
python examples/scrape_blog.py
```

Check the outputs:
- `data/processed/scraped_data.jsonl` - Raw scraped data
- `data/downloads/images/` - Downloaded images
- `.artifacts/web_scraper_graph.html` - Knowledge graph visualization

## Troubleshooting

### vLLM Issues
- **Out of memory**: Reduce `--max-model-len`
- **CUDA errors**: Check GPU availability
- **Slow inference**: Upgrade to better GPU

### Scrapy Issues
- **No data scraped**: Check robots.txt allows crawling
- **Rate limited**: Increase `DOWNLOAD_DELAY`
- **Import errors**: Activate virtual environment

### Cognee Issues
- **Ingestion fails**: Check database connectivity
- **No results**: Verify data was ingested
- **Search errors**: Check embedding model configuration

## Resources

- [Scrapy Documentation](https://docs.scrapy.org/)
- [Jina ReaderLM-v2](https://huggingface.co/jinaai/ReaderLM-v2)
- [vLLM Documentation](https://docs.vllm.ai/)
- [Cognee Documentation](https://docs.cognee.ai/)
- [robots.txt Specification](https://www.robotstxt.org/)
- [Sitemap Protocol](https://www.sitemaps.org/)

## License

Apache-2.0 (same as Cognee)

## Support

- Open issues on GitHub
- Check documentation
- Review examples

---

**Created**: October 2025  
**Status**: Complete and Ready to Use  
**Maintainer**: Cognee Community
