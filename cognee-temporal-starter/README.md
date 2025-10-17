# Cognee Temporal Aware Memory Starter

This folder contains examples and API extensions for **temporal aware memory handling** in cognee. It demonstrates how to use cognee's temporal graph capabilities to extract, store, and query events with temporal context.

## What is Temporal Aware Memory?

Temporal aware memory in cognee allows you to:
- Extract events and their timestamps from text
- Build knowledge graphs with temporal relationships
- Query information based on time ranges (e.g., "What happened between 1890 and 1900?")
- Track temporal entity relationships and event sequences

## Key Features

- **Temporal Event Extraction**: Automatically extract events with timestamps from documents
- **Time-Based Querying**: Search for events within specific time ranges
- **Temporal Relationships**: Track how entities and events relate over time
- **Temporal Cognify**: Enhanced cognify pipeline with temporal awareness enabled

## Getting Started

### Prerequisites

Follow the main cognee installation instructions from the parent repository. Make sure you have:

```bash
# Install cognee with dependencies
pip install -e ".[dev]"

# Set up your LLM API key
export LLM_API_KEY="your-api-key-here"
```

### Installation

Navigate to this directory:
```bash
cd cognee-temporal-starter
```

Install dependencies:
```bash
uv sync
```

Or with pip:
```bash
pip install -e .
```

### Quick Start

#### 1. Run the Basic Temporal Pipeline

Process historical biographies with temporal event extraction:

```bash
python src/pipelines/temporal_basic.py
```

This example:
- Ingests biographical text with dates and events
- Runs temporal cognify to extract events and timestamps
- Demonstrates temporal search queries

#### 2. Run the Temporal API Server

Start the extended API server with temporal endpoints:

```bash
python src/api/temporal_server.py
```

The server will start on `http://localhost:8000` with these additional endpoints:

- `POST /api/v1/temporal/cognify` - Run temporal cognify on datasets
- `POST /api/v1/temporal/search` - Search with temporal filters
- `POST /api/v1/temporal/events` - Query events by time range
- `GET /api/v1/temporal/timeline` - Get timeline view of events

## API Endpoints

### Temporal Cognify

Process datasets with temporal awareness enabled:

```bash
curl -X POST "http://localhost:8000/api/v1/temporal/cognify" \
  -H "Content-Type: application/json" \
  -d '{
    "datasets": ["historical_documents"]
  }'
```

### Temporal Search

Search with time range filters:

```bash
curl -X POST "http://localhost:8000/api/v1/temporal/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What events occurred?",
    "time_from": {"year": 1890, "month": 1, "day": 1},
    "time_to": {"year": 1900, "month": 12, "day": 31},
    "top_k": 10
  }'
```

### Query Events by Time Range

Get all events within a specific time period:

```bash
curl -X POST "http://localhost:8000/api/v1/temporal/events" \
  -H "Content-Type: application/json" \
  -d '{
    "time_from": {"year": 1985, "month": 1, "day": 1},
    "time_to": {"year": 1990, "month": 12, "day": 31}
  }'
```

### Get Timeline View

Retrieve a chronological timeline of events:

```bash
curl -X GET "http://localhost:8000/api/v1/temporal/timeline?dataset=my_dataset"
```

## Example Pipelines

### Basic Temporal Pipeline

The basic example (`src/pipelines/temporal_basic.py`) shows:
- How to enable temporal cognify
- Extracting events and timestamps
- Querying temporal information

### Advanced Temporal Pipeline

The advanced example (`src/pipelines/temporal_advanced.py`) demonstrates:
- Custom temporal models
- Event relationship tracking
- Complex temporal queries
- Visualization of temporal graphs

## How It Works

### 1. Temporal Event Extraction

When you run `cognify(temporal_cognify=True)`, cognee:

1. **Extracts Events**: Uses LLM to identify events in text
2. **Extracts Timestamps**: Identifies when events occurred
3. **Creates Event Nodes**: Stores events as graph nodes
4. **Links Entities**: Connects events to related entities
5. **Indexes Temporally**: Enables time-based queries

### 2. Temporal Search

The `TemporalRetriever` class:

1. **Extracts Time from Query**: Uses LLM to understand temporal context
2. **Filters by Time Range**: Finds events within the specified period
3. **Ranks Results**: Uses vector similarity for relevance
4. **Returns Context**: Provides temporal context for LLM completion

### 3. Temporal Models

Key models from `cognee.tasks.temporal_graph.models`:

- **Timestamp**: Represents a point in time (year, month, day, hour, minute, second)
- **Interval**: Represents a time range (starts_at, ends_at)
- **Event**: Represents an event with name, description, and temporal bounds
- **QueryInterval**: Used for temporal queries with optional time bounds

## Use Cases

### Historical Analysis
Analyze historical documents and timelines:
```python
await cognee.add(historical_documents)
await cognee.cognify(temporal_cognify=True)
results = await cognee.search(
    "What major events happened during World War II?",
    query_type=SearchType.TEMPORAL
)
```

### Biography Processing
Extract life events and timelines:
```python
results = await cognee.search(
    "What did this person do between 1990 and 2000?",
    query_type=SearchType.TEMPORAL
)
```

### News Analysis
Track events over time from news articles:
```python
await cognee.add(news_articles)
await cognee.cognify(temporal_cognify=True)
results = await cognee.search(
    "What happened in technology last month?",
    query_type=SearchType.TEMPORAL
)
```

## Architecture

```
cognee-temporal-starter/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── temporal_server.py      # Extended API server
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── temporal_cognify.py # Temporal cognify endpoint
│   │       ├── temporal_search.py  # Temporal search endpoint
│   │       └── temporal_events.py  # Event query endpoints
│   └── pipelines/
│       ├── temporal_basic.py       # Basic example
│       └── temporal_advanced.py    # Advanced example
├── README.md
└── pyproject.toml
```

## Integration with Cognee API

The temporal endpoints extend the standard cognee API server. They can be:

1. **Run Standalone**: Use `temporal_server.py` for dedicated temporal API
2. **Integrated**: Import routers into your main cognee API server
3. **Extended**: Build custom temporal endpoints using the provided examples

## References

- **Cognee Documentation**: https://docs.cognee.ai
- **Temporal Graph Tasks**: `cognee/tasks/temporal_graph/`
- **Temporal Retriever**: `cognee/modules/retrieval/temporal_retriever.py`
- **Test Examples**: `cognee/tests/test_temporal_graph.py`

## Contributing

Contributions are welcome! Please follow the main cognee contribution guidelines.

## License

Apache 2.0 - See LICENSE in the main repository
