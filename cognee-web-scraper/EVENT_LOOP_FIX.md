# Migration Guide - Event Loop Fix

## Issue

The original implementation used `CrawlerProcess` which starts Scrapy's Twisted reactor. This conflicts with asyncio's event loop when running inside an async function, causing:

```
RuntimeError: This event loop is already running
```

## Solution

**Changed**: Scrapy now runs in a separate subprocess instead of the same process.

### What Changed

**Before** (`CrawlerProcess` - Broken):
```python
from scrapy.crawler import CrawlerProcess

def run_scraper(self):
    process = CrawlerProcess(settings)
    process.crawl(spider_cls, ...)
    process.start()  # Blocks and conflicts with asyncio
```

**After** (Subprocess - Fixed):
```python
import subprocess

def run_scraper(self):
    # Creates temporary Python script
    # Runs Scrapy in separate subprocess
    result = subprocess.run([sys.executable, script_path])
```

## Benefits

1. ✅ **No Event Loop Conflicts**: Scrapy runs in its own process
2. ✅ **Better Isolation**: Crashes don't affect main process
3. ✅ **Async Compatible**: Works perfectly with asyncio
4. ✅ **Same Functionality**: No changes to API or usage

## Impact on Usage

**None!** The API is exactly the same:

```python
pipeline = WebScraperPipeline(
    start_urls=["https://example.com"],
)
await pipeline.run()  # Works now!
```

## Alternative Solutions Considered

### 1. CrawlerRunner (Not Used)
```python
from scrapy.crawler import CrawlerRunner
from twisted.internet import asyncioreactor
asyncioreactor.install()
```
**Rejected**: Still requires reactor management, complex setup

### 2. Crochet Library (Not Used)
```python
from crochet import setup as crochet_setup
crochet_setup()
```
**Rejected**: Extra dependency, still tricky with asyncio

### 3. Threading (Not Used)
```python
import threading
thread = threading.Thread(target=run_scraper)
```
**Rejected**: Thread safety issues with Twisted reactor

### 4. Subprocess (Chosen) ✅
**Advantages**:
- Clean separation
- No reactor conflicts
- Simple implementation
- Standard library only

## Technical Details

### How It Works

1. **Script Generation**: Creates temporary Python script with Scrapy crawler
2. **Subprocess Execution**: Runs script with `subprocess.run()`
3. **Output Capture**: Captures stdout/stderr for logging
4. **Result Collection**: Reads JSONL output file
5. **Cleanup**: Removes temporary script

### Error Handling

- Timeout after 1 hour (configurable)
- Captures and logs all output
- Propagates errors to main process
- Cleans up resources on failure

### Performance

- **Startup Overhead**: ~100-500ms (subprocess creation)
- **Memory**: Separate process memory space
- **CPU**: No difference from original

## Testing

All examples now work correctly:

```bash
# All of these work without event loop errors
python examples/simple_example.py
python examples/scrape_docs.py
python examples/scrape_blog.py
```

## Troubleshooting

### Issue: Subprocess Timeout
**Symptom**: `TimeoutExpired` error after 1 hour

**Solution**: Increase timeout in `scrape_website.py`:
```python
result = subprocess.run(
    [...],
    timeout=7200,  # 2 hours
)
```

### Issue: Permission Denied
**Symptom**: Can't create temporary file

**Solution**: Check temp directory permissions:
```bash
echo $TMPDIR  # Unix
echo %TEMP%   # Windows
```

### Issue: Module Not Found
**Symptom**: Import errors in subprocess

**Solution**: Ensure `src/` is in PYTHONPATH or use absolute imports

## Backward Compatibility

✅ **100% Compatible**: All existing code works without changes

The fix is completely transparent to users. No API changes, no behavior changes, just works!

## Future Improvements

Potential optimizations for future versions:

1. **Persistent Subprocess**: Keep subprocess alive for multiple crawls
2. **IPC Communication**: Real-time progress updates
3. **Distributed Crawling**: Multiple subprocesses for parallel crawling
4. **Resource Limits**: CPU/memory constraints for subprocess

## References

- [Scrapy Twisted Reactor Documentation](https://docs.scrapy.org/en/latest/topics/practices.html#run-scrapy-from-a-script)
- [Python subprocess Module](https://docs.python.org/3/library/subprocess.html)
- [Asyncio Event Loop](https://docs.python.org/3/library/asyncio-eventloop.html)
