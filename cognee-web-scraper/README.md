# Cognee Web Scraper

A comprehensive web scraping and crawling pipeline for Cognee that uses Scrapy for ethical web crawling and Jina ReaderLM-v2 for intelligent content extraction.

## Features

- **Ethical Web Crawling**: Respects robots.txt, sitemaps, and crawl delays
- **Intelligent Content Extraction**: Uses Jina ReaderLM-v2 for HTML-to-Markdown conversion
- **Image Downloading**: Automatically downloads and stores images
- **Content Cleanup**: LLM-based fact extraction and information cleanup
- **Cognee Integration**: Seamlessly ingests processed data into Cognee knowledge graphs

## Architecture

```
URL → Scrapy Spider → HTML/Images Download → ReaderLM-v2 Processing → Cognee Ingestion
```

### Components

1. **Scrapy Spider**: Crawls websites following best practices
2. **RobotsTxt Middleware**: Respects robots.txt exclusion rules
3. **Sitemap Spider**: Efficiently crawls using sitemap.xml
4. **Image Pipeline**: Downloads and stores images locally
5. **ReaderLM-v2 Processor**: Converts HTML to clean Markdown and extracts structured data
6. **Cognee Pipeline**: Ingests processed content into knowledge graph

## Installation

```bash
# Install dependencies
uv sync

# Install Playwright browsers (required for JavaScript-heavy sites)
playwright install
```

## Setup

### 1. Environment Variables

Create a `.env` file:

```bash
# vLLM Server Configuration (for local ReaderLM-v2)
VLLM_API_BASE=http://localhost:8000/v1
VLLM_MODEL_NAME=jinaai/ReaderLM-v2

# LLM for Cognee
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_API_KEY=your_api_key_here

# Embedding Configuration
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_API_KEY=your_api_key_here
```

### 2. Start ReaderLM-v2 Server

Start the vLLM server with ReaderLM-v2:

```bash
vllm serve jinaai/ReaderLM-v2 \
  --dtype auto \
  --api-key token-abc123 \
  --max-model-len 32768 \
  --port 8000
```

For production, use better hardware (RTX 3090/4090 recommended).

## Usage

### Basic Web Scraping

```bash
# Activate environment
source .venv/bin/activate  # Unix
# or
.venv\Scripts\activate  # Windows

# Run the scraper
python src/pipelines/scrape_website.py
```

### Custom Configuration

Edit `src/config/scraper_config.py` to customize:
- Start URLs
- Allowed domains
- Crawl depth and limits
- Download paths
- Processing options

## Pipeline Components

### 1. Scrapy Spider (`src/scraper/spiders/web_spider.py`)

- Follows links within allowed domains
- Respects robots.txt automatically
- Implements politeness delays
- Handles both regular and JavaScript-rendered pages

### 2. Sitemap Spider (`src/scraper/spiders/sitemap_spider.py`)

- Discovers URLs from sitemap.xml
- Follows sitemap indices
- Efficient for large sites

### 3. Content Processor (`src/processors/content_processor.py`)

- Uses ReaderLM-v2 for HTML→Markdown conversion
- Extracts structured facts using LLM
- Cleans and normalizes content

### 4. Cognee Pipeline (`src/pipelines/scrape_website.py`)

- Integrates with Cognee's data model
- Creates knowledge graph from extracted content
- Supports search and querying

## Configuration

### Scraper Settings (`src/scraper/settings.py`)

Key configurations:
- `ROBOTSTXT_OBEY = True`: Respects robots.txt
- `DOWNLOAD_DELAY = 2`: Polite crawling delay
- `CONCURRENT_REQUESTS = 8`: Parallel requests
- `DEPTH_LIMIT = 3`: Maximum crawl depth
- Image pipeline for downloading assets

### Content Processing

The pipeline uses ReaderLM-v2 with these capabilities:
- **HTML to Markdown**: Clean, structured content
- **Fact Extraction**: Identifies key information
- **Multi-language**: Supports 29 languages
- **Long Context**: Handles up to 512K tokens

## Best Practices

### Ethical Crawling

1. **Always respect robots.txt**
2. **Set appropriate delays** (default: 2 seconds)
3. **Limit crawl depth** to avoid overloading servers
4. **Use a descriptive User-Agent** string
5. **Handle errors gracefully** and retry appropriately

### Performance

1. **Use sitemap when available** for efficiency
2. **Cache downloaded content** to avoid re-crawling
3. **Process in batches** for large sites
4. **Monitor resource usage** (CPU, memory, bandwidth)

## Project Structure

```
cognee-web-scraper/
├── src/
│   ├── scraper/
│   │   ├── spiders/
│   │   │   ├── web_spider.py          # Main crawling spider
│   │   │   └── sitemap_spider.py      # Sitemap-based spider
│   │   ├── middlewares.py             # Custom middlewares
│   │   ├── pipelines.py               # Scrapy pipelines
│   │   └── settings.py                # Scrapy settings
│   ├── processors/
│   │   ├── content_processor.py       # ReaderLM-v2 integration
│   │   └── fact_extractor.py          # LLM-based fact extraction
│   ├── models/
│   │   └── data_models.py             # Cognee data models
│   ├── config/
│   │   └── scraper_config.py          # Configuration
│   └── pipelines/
│       └── scrape_website.py          # Main Cognee pipeline
├── data/
│   ├── downloads/                     # Downloaded HTML/images
│   └── processed/                     # Processed content
├── .env.template                      # Environment template
├── .gitignore
├── pyproject.toml
└── README.md
```

## Examples

### Example 1: Scrape Documentation Site

```python
from cognee_web_scraper import run_scraper

await run_scraper(
    start_urls=['https://docs.example.com'],
    allowed_domains=['docs.example.com'],
    crawl_depth=2
)
```

### Example 2: Extract Facts from News Site

```python
results = await scrape_and_extract(
    url='https://news.example.com/article',
    extract_facts=True,
    save_images=True
)
```

## Troubleshooting

### RuntimeError: This event loop is already running

**Cause**: Scrapy's Twisted reactor conflicts with asyncio event loop  
**Solution**: ✅ Pipeline uses subprocess-based execution to isolate event loops  
**Implementation**: See `src/pipelines/scrape_website.py` - Scrapy runs in separate process

### Deprecation Warnings (FIXED)

✅ **FEED_URI/FEED_FORMAT**: Replaced with `FEEDS` dictionary (Scrapy 2.1+)  
✅ **offsite middleware**: Removed deprecated spider middleware  
All settings now use current Scrapy best practices.

### vLLM Installation/Compatibility

**Windows**: vLLM is NOT compatible with Windows  
- **Solution**: Use WSL2, Linux VM, or macOS
- **Testing**: You can test Scrapy portion independently (vLLM optional)

**Linux/macOS**:
- Requires CUDA 11.8+ for GPU support
- Check CUDA: `nvidia-smi`
- At least 8GB VRAM for ReaderLM-v2

**Out of Memory**: Reduce context length:
```bash
vllm serve jinaai/ReaderLM-v2 --max-model-len 16384
```

### Scrapy Rate Limiting

Adjust settings in `settings.py`:
```python
DOWNLOAD_DELAY = 5  # Increase delay
CONCURRENT_REQUESTS = 4  # Reduce concurrency
```

### Content Processing Fails

1. **Verify vLLM running**: `curl http://localhost:8000/v1/models`
2. **Check server logs**: Watch vLLM terminal for errors
3. **Test endpoint**: 
```python
from processors.content_processor import ContentProcessor
import asyncio
processor = ContentProcessor()
asyncio.run(processor.html_to_markdown('<h1>Test</h1>'))
```

### Playwright Issues

Reinstall browsers:
```bash
playwright install --force
```

## License

Apache-2.0

## References

- [Scrapy Documentation](https://docs.scrapy.org/)
- [Jina AI ReaderLM-v2](https://huggingface.co/jinaai/ReaderLM-v2)
- [vLLM Documentation](https://docs.vllm.ai/)
- [Cognee Documentation](https://docs.cognee.ai/)
