# Testing Guide for Cognee Temporal Starter

This guide explains how to test the temporal aware memory features.

## Prerequisites

Ensure you have cognee installed and configured:

```bash
# Install cognee with dev dependencies
cd /home/runner/work/cognee/cognee
pip install -e ".[dev]"

# Or using uv (recommended)
uv pip install -e ".[dev]"
```

Set up your environment:

```bash
cd cognee-temporal-starter
cp .env.template .env
# Edit .env and add your LLM_API_KEY
```

## Testing Pipeline Examples

### 1. Test Basic Temporal Pipeline

This example demonstrates basic temporal event extraction and querying:

```bash
cd cognee-temporal-starter
python src/pipelines/temporal_basic.py
```

**Expected Output:**
- Successful data ingestion
- Temporal cognify completion
- Query results for Marie Curie's life events
- Events filtered by time ranges (1900-1910, WWI period, etc.)

**What It Tests:**
- ✓ Event extraction from biographical text
- ✓ Timestamp parsing and storage
- ✓ Temporal search with natural language queries
- ✓ Time range filtering

### 2. Test Advanced Temporal Pipeline

This example shows complex multi-dataset temporal processing:

```bash
cd cognee-temporal-starter
python src/pipelines/temporal_advanced.py
```

**Expected Output:**
- Processing of two datasets (WWII history + Tech history)
- Multiple temporal queries across different time periods
- Graph statistics showing Events and Timestamps
- HTML visualization of the temporal graph

**What It Tests:**
- ✓ Multi-dataset temporal cognify
- ✓ Cross-dataset temporal queries
- ✓ Complex time range queries (decades, specific years)
- ✓ Graph structure validation
- ✓ Visualization generation

## Testing API Endpoints

### Start the Temporal API Server

```bash
cd cognee-temporal-starter
python src/api/temporal_server.py
```

The server will start on `http://localhost:8000`

### Test Individual Endpoints

#### 1. Health Check

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "temporal-api"
}
```

#### 2. Temporal Cognify

First, add some data using the standard add endpoint, then run temporal cognify:

```bash
# Add data (requires authentication token in production)
curl -X POST "http://localhost:8000/api/v1/temporal/cognify" \
  -H "Content-Type: application/json" \
  -d '{
    "datasets": ["test_dataset"]
  }'
```

**Expected Response:**
```json
{
  "message": "Temporal cognify completed successfully",
  "datasets_processed": ["test_dataset"],
  "status": "success"
}
```

#### 3. Temporal Search

```bash
curl -X POST "http://localhost:8000/api/v1/temporal/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What happened in the 1990s?",
    "datasets": ["test_dataset"],
    "top_k": 10
  }'
```

**Expected Response:**
List of search results with temporal context.

#### 4. Query Events by Time Range

```bash
curl -X POST "http://localhost:8000/api/v1/temporal/events" \
  -H "Content-Type: application/json" \
  -d '{
    "time_from": {"year": 1990, "month": 1, "day": 1},
    "time_to": {"year": 2000, "month": 12, "day": 31},
    "limit": 50
  }'
```

**Expected Response:**
```json
{
  "events": [
    {
      "id": "...",
      "name": "Event name",
      "description": "Event description",
      "time_from": {"year": 1991, "month": 8, "day": 6},
      "time_to": null,
      "location": null
    }
  ],
  "total_count": 10,
  "time_range": {
    "time_from": {"year": 1990, "month": 1, "day": 1},
    "time_to": {"year": 2000, "month": 12, "day": 31}
  }
}
```

#### 5. Get Timeline

```bash
curl "http://localhost:8000/api/v1/temporal/timeline?dataset=test_dataset"
```

## Validation Checklist

### Code Quality
- [x] All Python files have valid syntax
- [x] Import statements are correct
- [x] Type hints are properly used
- [x] Error handling is implemented

### Functionality
- [ ] Basic pipeline runs without errors
- [ ] Advanced pipeline runs without errors
- [ ] API server starts successfully
- [ ] All API endpoints respond correctly
- [ ] Temporal cognify processes data
- [ ] Temporal search returns relevant results
- [ ] Event queries filter by time range
- [ ] Timeline endpoint returns data

### Integration
- [ ] Integrates with existing cognee API
- [ ] Uses TemporalRetriever correctly
- [ ] Leverages temporal_graph tasks
- [ ] Follows cognee patterns and conventions

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution:** Ensure cognee is installed:
```bash
cd /home/runner/work/cognee/cognee
pip install -e ".[dev]"
```

### Issue: LLM API Key Error

**Solution:** Set your API key in .env:
```bash
export LLM_API_KEY="your-key-here"
```

### Issue: Database Connection Error

**Solution:** The examples use default local databases (kuzu, lancedb). Ensure they can be created in the .cognee_system directory.

### Issue: Empty Search Results

**Solution:** 
1. Verify data was added successfully
2. Ensure temporal_cognify=True was used
3. Check that your query contains temporal information
4. Try with a broader time range

## Manual Testing Scenarios

### Scenario 1: Historical Document Analysis

1. Add historical documents with dates
2. Run temporal cognify
3. Query: "What happened between 1940 and 1945?"
4. Verify results contain WWII events

### Scenario 2: Biography Timeline

1. Add biographical text
2. Run temporal cognify
3. Query: "What did this person do in the 1990s?"
4. Verify results are chronologically filtered

### Scenario 3: Cross-Dataset Temporal Search

1. Add multiple datasets with different time periods
2. Run temporal cognify on all
3. Query across multiple datasets
4. Verify results from both datasets

## Performance Testing

### Load Test for API

```bash
# Install Apache Bench if not available
# apt-get install apache2-utils

# Test temporal search endpoint
ab -n 100 -c 10 -p payload.json -T application/json \
  http://localhost:8000/api/v1/temporal/search
```

### Stress Test for Pipeline

Process large datasets to test scalability:

```python
import asyncio
from cognee import add, cognify

async def stress_test():
    # Add large document collection
    large_dataset = [doc for doc in large_document_collection]
    await add(large_dataset, "large_temporal_test")
    
    # Run temporal cognify
    await cognify(datasets=["large_temporal_test"], temporal_cognify=True)

asyncio.run(stress_test())
```

## Automated Testing

To add automated tests, create a test file:

```python
# tests/test_temporal_api.py
import pytest
from fastapi.testclient import TestClient
from src.api.temporal_server import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_temporal_cognify():
    response = client.post(
        "/api/v1/temporal/cognify",
        json={"datasets": ["test_dataset"]}
    )
    assert response.status_code == 200

# Add more tests...
```

Run tests with pytest:
```bash
pytest tests/test_temporal_api.py
```

## Expected Results Summary

When all tests pass, you should see:

1. **Pipeline Examples:**
   - ✓ Events extracted from text
   - ✓ Timestamps correctly parsed
   - ✓ Temporal queries return relevant results
   - ✓ Graph visualization created

2. **API Endpoints:**
   - ✓ Server starts without errors
   - ✓ All endpoints return 200 OK
   - ✓ Temporal cognify processes data
   - ✓ Temporal search filters by time
   - ✓ Event queries return structured data

3. **Integration:**
   - ✓ Works with existing cognee infrastructure
   - ✓ Follows cognee patterns
   - ✓ Uses standard authentication
   - ✓ Compatible with all database providers

## Reporting Issues

If you encounter issues:

1. Check the logs for error messages
2. Verify all prerequisites are met
3. Ensure API keys are configured
4. Try with a minimal example first
5. Report issues with full error traces and steps to reproduce
