# Quick Start Guide

## 1. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## 2. Start ReaderLM-v2 Server

```bash
# Install vLLM if not already installed
pip install vllm

# Start the server
vllm serve jinaai/ReaderLM-v2 \
  --dtype auto \
  --api-key token-abc123 \
  --max-model-len 32768 \
  --port 8000
```

## 3. Configure Environment

```bash
# Copy template
cp .env.template .env

# Edit .env with your settings
# At minimum, set your LLM API keys
```

## 4. Run Example

```bash
# Activate environment
source .venv/bin/activate  # Unix
# or
.venv\Scripts\activate  # Windows

# Run example scraper
python src/pipelines/scrape_website.py
```

## 5. Query Knowledge Graph

After scraping, you can query the knowledge graph:

```python
from pipelines.scrape_website import WebScraperPipeline
import asyncio

async def query_example():
    pipeline = WebScraperPipeline(
        start_urls=["https://example.com"],
    )
    
    # Assuming data is already scraped
    result = await pipeline.query("What information is available?")
    print(result)

asyncio.run(query_example())
```

## Troubleshooting

### vLLM won't start

**Problem**: Out of memory or CUDA errors

**Solution**: Reduce context length:
```bash
vllm serve jinaai/ReaderLM-v2 --max-model-len 8192
```

### Scrapy errors

**Problem**: Import errors or module not found

**Solution**: Ensure you're in the project directory and environment is activated:
```bash
cd cognee-web-scraper
source .venv/bin/activate
python -m scrapy version  # Should show version
```

### No data scraped

**Problem**: robots.txt blocking or rate limiting

**Solution**: 
1. Check robots.txt of target site
2. Increase download delay in settings.py
3. Check site allows crawling

## Next Steps

1. Customize scraper configuration in `src/config/scraper_config.py`
2. Explore examples in `examples/` directory
3. Read full documentation in README.md
4. Check Scrapy and Cognee documentation for advanced features
