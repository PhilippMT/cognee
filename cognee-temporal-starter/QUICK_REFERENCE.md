# Quick Reference Guide

## Temporal Aware Memory - Quick Commands

### Setup

```bash
# Navigate to temporal starter
cd cognee-temporal-starter

# Install dependencies
uv sync
# or
pip install -e .

# Configure environment
cp .env.template .env
# Edit .env and set LLM_API_KEY
```

### Run Examples

```bash
# Basic example (Marie Curie biography)
python src/pipelines/temporal_basic.py

# Advanced example (WWII + Tech history)
python src/pipelines/temporal_advanced.py
```

### Start API Server

```bash
# Start temporal API server
python src/api/temporal_server.py

# Server will be available at http://localhost:8000
```

### API Endpoints Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/temporal/cognify` | POST | Run temporal cognify on datasets |
| `/api/v1/temporal/search` | POST | Search with temporal filters |
| `/api/v1/temporal/events` | POST | Query events by time range |
| `/api/v1/temporal/timeline` | GET | Get chronological timeline |

### Python Usage

```python
import asyncio
from cognee import add, prune, SearchType
from cognee.api.v1.cognify import cognify
from cognee.api.v1.search import search

async def temporal_example():
    # Clean up
    await prune.prune_data()
    await prune.prune_system(metadata=True)
    
    # Add data
    text = "Marie Curie was born on November 7, 1867..."
    await add([text], dataset_name="biography")
    
    # Run temporal cognify
    await cognify(datasets=["biography"], temporal_cognify=True)
    
    # Search with temporal awareness
    results = await search(
        query_text="What happened in the 1900s?",
        query_type=SearchType.TEMPORAL,
        datasets=["biography"]
    )
    
    print(results)

asyncio.run(temporal_example())
```

### cURL Examples

```bash
# Temporal Cognify
curl -X POST "http://localhost:8000/api/v1/temporal/cognify" \
  -H "Content-Type: application/json" \
  -d '{"datasets": ["my_dataset"]}'

# Temporal Search
curl -X POST "http://localhost:8000/api/v1/temporal/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What events occurred in the 1990s?",
    "datasets": ["my_dataset"],
    "top_k": 10
  }'

# Query Events by Time Range
curl -X POST "http://localhost:8000/api/v1/temporal/events" \
  -H "Content-Type: application/json" \
  -d '{
    "time_from": {"year": 1990, "month": 1, "day": 1},
    "time_to": {"year": 2000, "month": 12, "day": 31},
    "limit": 50
  }'

# Get Timeline
curl "http://localhost:8000/api/v1/temporal/timeline?dataset=my_dataset"
```

### Key Models

```python
from cognee.tasks.temporal_graph.models import Timestamp, Event, QueryInterval

# Timestamp
timestamp = Timestamp(
    year=1991,
    month=8,
    day=6,
    hour=0,
    minute=0,
    second=0
)

# Event
event = Event(
    name="World Wide Web made public",
    description="Tim Berners-Lee released the WWW to the public",
    time_from=timestamp,
    time_to=None,
    location="CERN, Switzerland"
)

# Query Interval (for temporal queries)
query_interval = QueryInterval(
    starts_at=Timestamp(year=1990, month=1, day=1),
    ends_at=Timestamp(year=2000, month=12, day=31)
)
```

### Common Temporal Queries

```python
# Query by decade
"What happened in the 1990s?"

# Query by specific years
"What happened between 1939 and 1945?"

# Query by event type
"When was the first iPhone released?"

# Query by person
"What did Marie Curie do in 1903?"

# Query before/after date
"What happened before 1900?"
"What happened after 2000?"
```

### Troubleshooting Quick Fixes

```bash
# Import error
pip install -e ".[dev]"

# API key error
export LLM_API_KEY="your-key-here"

# Database error
rm -rf .cognee_system
# Then re-run

# Clear data
python -c "import asyncio; from cognee import prune; asyncio.run(prune.prune_data()); asyncio.run(prune.prune_system(metadata=True))"
```

### Directory Structure

```
cognee-temporal-starter/
├── README.md              # Full documentation
├── TESTING.md             # Testing guide
├── QUICK_REFERENCE.md     # This file
├── .env.template          # Environment template
├── pyproject.toml         # Dependencies
└── src/
    ├── api/
    │   ├── temporal_server.py           # Main API server
    │   └── routers/
    │       ├── temporal_cognify.py      # Cognify endpoint
    │       ├── temporal_search.py       # Search endpoint
    │       └── temporal_events.py       # Events endpoint
    └── pipelines/
        ├── temporal_basic.py            # Basic example
        └── temporal_advanced.py         # Advanced example
```

### Integration with Main Cognee API

To add temporal endpoints to the main cognee API server:

```python
# In cognee/api/client.py
from cognee_temporal_starter.src.api import (
    get_temporal_cognify_router,
    get_temporal_search_router,
    get_temporal_events_router,
)

# Add to router includes
app.include_router(
    get_temporal_cognify_router(),
    prefix="/api/v1/temporal/cognify",
    tags=["temporal"]
)
app.include_router(
    get_temporal_search_router(),
    prefix="/api/v1/temporal/search",
    tags=["temporal"]
)
app.include_router(
    get_temporal_events_router(),
    prefix="/api/v1/temporal/events",
    tags=["temporal"]
)
```

### Resources

- Main README: `README.md`
- Testing Guide: `TESTING.md`
- Cognee Docs: https://docs.cognee.ai
- Temporal Graph Tasks: `cognee/tasks/temporal_graph/`
- Temporal Retriever: `cognee/modules/retrieval/temporal_retriever.py`
