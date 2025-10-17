# Cognee Temporal Starter - Project Overview

## What is This?

This is a dedicated extension package for **cognee** that provides temporal-aware memory handling capabilities through:
- Extended API endpoints for temporal operations
- Example pipelines demonstrating temporal features
- Comprehensive documentation and testing guides

## Quick Start (3 Steps)

### 1. Setup
```bash
cd cognee-temporal-starter
cp .env.template .env
# Add your LLM_API_KEY to .env
pip install -e .
```

### 2. Run an Example
```bash
python src/pipelines/temporal_basic.py
```

### 3. Start the API Server
```bash
python src/api/temporal_server.py
# Access at http://localhost:8000
```

## What Can You Do?

### Extract Events from Text
```python
# Input: "Marie Curie won the Nobel Prize in 1903"
# Output: Event(name="Nobel Prize", time_from=Timestamp(year=1903))
```

### Query by Time Range
```python
results = await search(
    "What happened between 1990 and 2000?",
    query_type=SearchType.TEMPORAL
)
```

### Build Timelines
```python
# Get all events in chronological order
timeline = await get_timeline(dataset="history")
```

## File Guide

| File | Purpose |
|------|---------|
| `README.md` | 📖 Complete documentation (252 lines) |
| `QUICK_REFERENCE.md` | ⚡ Quick commands and snippets (236 lines) |
| `TESTING.md` | ✅ Testing guide and validation (345 lines) |
| `src/pipelines/temporal_basic.py` | 🔰 Basic example - biography processing |
| `src/pipelines/temporal_advanced.py` | 🚀 Advanced example - multi-dataset analysis |
| `src/api/temporal_server.py` | 🌐 API server with temporal endpoints |
| `src/api/routers/temporal_*.py` | 🔌 Individual endpoint implementations |

## Key Concepts

### Temporal Cognify
Process documents to extract events with timestamps:
```bash
POST /api/v1/temporal/cognify
{"datasets": ["my_dataset"]}
```

### Temporal Search
Search with time awareness:
```bash
POST /api/v1/temporal/search
{
  "query": "What happened in the 1990s?",
  "top_k": 10
}
```

### Event Queries
Get events in specific time ranges:
```bash
POST /api/v1/temporal/events
{
  "time_from": {"year": 1990, "month": 1, "day": 1},
  "time_to": {"year": 2000, "month": 12, "day": 31}
}
```

## Architecture

```
User Query
    ↓
Temporal API Endpoints
    ↓
TemporalRetriever (extracts time from query)
    ↓
Graph Engine (filters events by time)
    ↓
Vector Search (ranks by relevance)
    ↓
LLM Completion (generates answer)
    ↓
Results
```

## Integration with Cognee

This package uses cognee's existing temporal infrastructure:

- **Tasks**: `cognee.tasks.temporal_graph.*`
  - Extract events and timestamps
  - Build temporal relationships

- **Retrieval**: `cognee.modules.retrieval.temporal_retriever.TemporalRetriever`
  - Time-aware search
  - Context extraction

- **Models**: `cognee.tasks.temporal_graph.models`
  - `Timestamp` - Point in time
  - `Event` - Named event with time bounds
  - `QueryInterval` - Time range for queries

## Use Cases

### 📚 Historical Analysis
Process historical documents and query by time period.

### 👤 Biography Processing  
Extract life events and create timelines.

### 📰 News Analysis
Track events over time from news articles.

### 💼 Business Events
Monitor company milestones and market events.

### 🔬 Research Timeline
Track scientific discoveries and publications.

## What's Different from Standard Cognee?

| Standard Cognee | Temporal Starter |
|----------------|------------------|
| General knowledge graph | Time-aware knowledge graph |
| Semantic search | Semantic + temporal search |
| No time filtering | Query by time range |
| Entity relationships | Entity + event relationships |
| N/A | Dedicated temporal API endpoints |

## Where to Go From Here

1. **New to Temporal Features?**
   → Start with `README.md` for full explanation

2. **Want to Test It?**
   → Check `TESTING.md` for validation steps

3. **Need Quick Reference?**
   → Use `QUICK_REFERENCE.md` for commands

4. **Ready to Build?**
   → Run examples in `src/pipelines/`

5. **Want API Integration?**
   → Start server with `src/api/temporal_server.py`

## Technical Details

- **Language**: Python 3.10+
- **Framework**: FastAPI for API
- **Dependencies**: cognee (parent project)
- **Databases**: kuzu (graph), lancedb (vector)
- **LLM**: OpenAI (configurable)

## Support

- **Issues**: Report in main cognee repository
- **Questions**: Discord - https://discord.gg/NQPKmU5CCg
- **Docs**: https://docs.cognee.ai

## License

Apache 2.0 (same as cognee)

---

**Last Updated**: 2025-10-17  
**Version**: 0.1.0  
**Status**: ✅ Ready to use
