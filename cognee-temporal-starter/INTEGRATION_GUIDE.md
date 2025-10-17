# Integration Guide: Adding Temporal Endpoints to Main Cognee API

## Overview

This guide shows how to integrate temporal endpoints into the main cognee API server **without changing any code outside of cognee-temporal-starter**.

## Method: Import-Based Integration

The temporal routers are designed to be importable and used in the main API server through Python imports.

## Step-by-Step Integration

### Step 1: Install cognee-temporal-starter

```bash
# From cognee root directory
pip install -e ./cognee-temporal-starter
```

This makes the package importable as `cognee_temporal_starter`.

### Step 2: Import Temporal Routers in Main API

In your main API server file (e.g., when running cognee API), add the imports:

```python
# Example: In your custom server file or after importing cognee.api.client

from fastapi import FastAPI
from cognee.api.client import app  # Main cognee API app

# Import temporal routers
try:
    from cognee_temporal_starter.src.api import (
        get_temporal_cognify_router,
        get_temporal_search_router,
        get_temporal_events_router,
    )
    
    # Register temporal endpoints
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
    
    print("✓ Temporal endpoints registered successfully")
    
except ImportError as e:
    print(f"⚠ Temporal starter not available: {e}")
    print("  Install with: pip install -e ./cognee-temporal-starter")
```

### Step 3: Start the API Server

```python
# Standard cognee API start
from cognee.api.client import start_api_server

# The temporal endpoints are now available
start_api_server(host="0.0.0.0", port=8000)
```

## Alternative: Standalone Temporal Server

If you prefer to run temporal endpoints separately:

```bash
cd cognee-temporal-starter
python src/api/temporal_server.py
```

This starts a server on port 8000 with:
- All standard cognee endpoints
- All temporal endpoints
- Independent from main API

## Verification

After integration, verify endpoints are available:

```bash
# Check API docs
curl http://localhost:8000/docs

# Test temporal cognify endpoint
curl -X POST "http://localhost:8000/api/v1/temporal/cognify" \
  -H "Content-Type: application/json" \
  -d '{"datasets": ["test"]}'

# Test temporal search endpoint
curl -X POST "http://localhost:8000/api/v1/temporal/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "What happened?", "top_k": 10}'
```

## Benefits of This Approach

✅ **No Code Changes Outside cognee-temporal-starter**
- Main cognee code remains untouched
- Clean separation of concerns
- Easy to maintain

✅ **Optional Integration**
- Users can choose to install temporal-starter or not
- Graceful degradation if not installed
- No breaking changes

✅ **No Code Duplication**
- Single source of truth for temporal endpoints
- Changes in temporal-starter automatically reflected
- Consistent behavior

✅ **Flexible Deployment**
- Can run integrated with main API
- Can run as standalone service
- Can run both simultaneously

## Advanced: Custom Integration Script

Create a custom integration script:

```python
# integrate_temporal.py
"""
Custom script to run cognee API with temporal endpoints.
"""
import sys
from cognee.api.client import app

def integrate_temporal_endpoints():
    """Add temporal endpoints to the cognee API."""
    try:
        from cognee_temporal_starter.src.api import (
            get_temporal_cognify_router,
            get_temporal_search_router,
            get_temporal_events_router,
        )
        
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
        
        print("✓ Temporal endpoints integrated")
        return True
        
    except ImportError as e:
        print(f"✗ Could not integrate temporal endpoints: {e}")
        print("  Install with: pip install -e ./cognee-temporal-starter")
        return False

if __name__ == "__main__":
    integrate_temporal_endpoints()
    
    # Start the server
    from cognee.api.client import start_api_server
    start_api_server()
```

Usage:
```bash
python integrate_temporal.py
```

## Docker Integration

If using Docker, update your Dockerfile:

```dockerfile
# Dockerfile
FROM python:3.10

# Install main cognee
COPY . /app
WORKDIR /app
RUN pip install -e .

# Install temporal starter (optional)
RUN pip install -e ./cognee-temporal-starter

# Your integration script
COPY integrate_temporal.py /app/
CMD ["python", "integrate_temporal.py"]
```

## Environment Variables

No additional environment variables needed beyond standard cognee configuration:

```bash
# .env
LLM_API_KEY=your_key_here
LLM_PROVIDER=openai
LLM_MODEL=gpt-4

# Optional: Specify graph/vector DB
GRAPH_DATABASE_PROVIDER=kuzu
VECTOR_DB_PROVIDER=lancedb
```

## Troubleshooting

### Issue: ImportError when importing temporal routers

**Solution**: Install cognee-temporal-starter
```bash
pip install -e ./cognee-temporal-starter
```

### Issue: Endpoints not showing in /docs

**Solution**: Verify routers are registered before starting server
```python
# Check registration before starting
print(app.routes)  # Should show temporal routes
```

### Issue: Authentication errors

**Solution**: Temporal endpoints use cognee's standard authentication. Ensure:
- User is authenticated
- API keys are set
- Permissions are correct

## Production Deployment

### Option 1: Integrated Deployment
```bash
# Install both packages
pip install cognee
pip install -e ./cognee-temporal-starter

# Use custom start script with integration
python integrate_temporal.py
```

### Option 2: Separate Services
```bash
# Service 1: Main cognee API
python -m cognee.api.client

# Service 2: Temporal API (different port)
cd cognee-temporal-starter && python src/api/temporal_server.py
```

### Option 3: Docker Compose
```yaml
version: '3.8'
services:
  cognee-main:
    build: .
    ports:
      - "8000:8000"
    command: python -m cognee.api.client
    
  cognee-temporal:
    build: .
    ports:
      - "8001:8000"
    working_dir: /app/cognee-temporal-starter
    command: python src/api/temporal_server.py
```

## Summary

**Key Points**:
1. No code changes needed outside `cognee-temporal-starter/`
2. Integration via Python imports only
3. Optional installation - doesn't break main API
4. Can run integrated or standalone
5. Zero code duplication

**Recommended Approach**: Import-based integration with try/except for graceful degradation.
