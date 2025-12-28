# ADHD Thought Graph API Documentation

## Overview

The Thought Graph API provides RESTful endpoints for managing ADHD-optimized thought graphs with automatic connection discovery, graph enrichment, web research integration, project matching, and edge weight management.

**Base URL**: `/api/v1/thought_graph`

**Authentication**: All endpoints require authentication via Bearer token or Cookie (same as other Cognee API endpoints).

## Features

- **Thought Management**: Capture and organize thoughts with ADHD-optimized fields
- **Connection Discovery**: Automatic semantic and tag-based relationship finding
- **Graph Enrichment**: PageRank, centrality, community detection, transitive connections
- **Web Research**: Enrich thoughts with external knowledge via Tavily API
- **Project Matching**: Auto-detect and link GitHub/GitLab repositories
- **Edge Management**: Time-based decay, reinforcement, potential connections
- **Integrated Memify**: One-command comprehensive enrichment

---

## Endpoints

### Thought Management

#### POST `/api/v1/thought_graph/thoughts`
Add a new thought to the graph.

**Request Body**:
```json
{
  "content": "Build a graph database for ADHD thought management",
  "tags": ["adhd", "productivity", "graph-db"],
  "energy_level": 7,
  "importance_score": 9,
  "auto_connect": true,
  "similarity_threshold": 0.7
}
```

**Response**: `ThoughtResponseDTO`
```json
{
  "id": "thought_abc123",
  "content": "Build a graph database for ADHD thought management",
  "tags": ["adhd", "productivity", "graph-db"],
  "energy_level": 7,
  "importance_score": 9,
  "created_at": "2025-12-28T19:00:00Z",
  "updated_at": "2025-12-28T19:00:00Z",
  "pagerank_score": null,
  "betweenness_centrality": null,
  "community_id": null
}
```

**Parameters**:
- `content` (required): Thought content text
- `tags` (optional): List of tags for categorization
- `energy_level` (optional): Energy level 1-10 when thought was captured
- `importance_score` (optional): Importance rating 1-10
- `auto_connect` (optional, default: true): Automatically discover connections
- `similarity_threshold` (optional, default: 0.7): Minimum similarity for auto-connections (0.0-1.0)

**Error Codes**:
- `400`: Invalid parameters (empty content, out-of-range values)
- `409`: Error during creation
- `500`: Unexpected error

---

#### POST `/api/v1/thought_graph/thoughts/batch`
Add multiple thoughts in batch.

**Request Body**:
```json
{
  "thoughts": [
    {
      "content": "First thought",
      "tags": ["tag1"],
      "importance_score": 7
    },
    {
      "content": "Second thought",
      "tags": ["tag2"],
      "energy_level": 6
    }
  ]
}
```

**Response**: `List[ThoughtResponseDTO]`

**Error Codes**:
- `400`: Invalid parameters
- `409`: Error during batch creation

---

### Connection Discovery

#### POST `/api/v1/thought_graph/connections/discover`
Discover connections for a specific thought.

**Request Body**:
```json
{
  "thought_id": "thought_abc123",
  "similarity_threshold": 0.7,
  "max_connections": 10
}
```

**Response**: `List[ConnectionResponseDTO]`
```json
[
  {
    "source_id": "thought_abc123",
    "target_id": "thought_xyz789",
    "relationship_type": "semantic_similarity",
    "discovery_method": "vector_search",
    "strength": 0.85,
    "explanation": "Both discuss graph databases and ADHD tools"
  }
]
```

**Parameters**:
- `thought_id` (required): Thought ID to discover connections for
- `similarity_threshold` (optional, default: 0.7): Minimum similarity (0.0-1.0)
- `max_connections` (optional, default: 10): Maximum connections to discover

**Error Codes**:
- `404`: Thought ID doesn't exist
- `409`: Error during connection discovery

---

#### GET `/api/v1/thought_graph/connections/surprise`
Find surprise connections with high semantic or temporal distance.

**Query Parameters**:
- `min_surprise_score` (optional, default: 0.6): Minimum surprise score
- `limit` (optional, default: 10): Maximum results to return

**Response**: `List[SurpriseConnectionResponseDTO]`
```json
[
  {
    "thought1_id": "thought_abc123",
    "thought2_id": "thought_def456",
    "surprise_score": 0.82,
    "semantic_distance": 0.75,
    "temporal_distance": 45.5,
    "explanation": "Unexpected connection between ADHD tools and machine learning"
  }
]
```

**Error Codes**:
- `409`: Error finding surprise connections

---

### Graph Enrichment

#### POST `/api/v1/thought_graph/enrich`
Enrich the graph with algorithms.

**Request Body**:
```json
{
  "compute_pagerank": true,
  "compute_centrality": true,
  "detect_communities": true,
  "find_transitive": true,
  "auto_add_transitive_links": false
}
```

**Response**: `EnrichmentResultsResponseDTO`
```json
{
  "pagerank_scores": {
    "thought_abc123": 0.15,
    "thought_xyz789": 0.10
  },
  "centrality_scores": {
    "betweenness": {"thought_abc123": 0.25},
    "closeness": {"thought_abc123": 0.40}
  },
  "communities": {
    "0": ["thought_abc123", "thought_xyz789"],
    "1": ["thought_def456"]
  },
  "transitive_connections": [
    {
      "source": "thought_abc123",
      "target": "thought_ghi012",
      "intermediate": "thought_xyz789"
    }
  ],
  "processing_time": 2.45
}
```

**Parameters**:
- `compute_pagerank` (optional, default: true): Compute PageRank scores
- `compute_centrality` (optional, default: true): Compute centrality measures
- `detect_communities` (optional, default: true): Detect thought communities
- `find_transitive` (optional, default: true): Find transitive connections
- `auto_add_transitive_links` (optional, default: false): Auto-create transitive links

**Error Codes**:
- `409`: Error during graph enrichment

---

### Web Enrichment

#### POST `/api/v1/thought_graph/enrich/web`
Enrich a thought with web search results.

**Requirements**: `TAVILY_API_KEY` environment variable must be set.

**Request Body**:
```json
{
  "thought_id": "thought_abc123",
  "max_results": 5,
  "search_depth": "basic"
}
```

**Response**: `WebEnrichmentResponseDTO`
```json
{
  "thought_id": "thought_abc123",
  "search_results": [
    {
      "title": "ADHD and Graph Databases",
      "url": "https://example.com/article",
      "snippet": "How graph databases help ADHD..."
    }
  ],
  "enrichment_status": "completed"
}
```

**Parameters**:
- `thought_id` (required): Thought ID to enrich
- `max_results` (optional, default: 5): Maximum search results (1-20)
- `search_depth` (optional, default: "basic"): "basic" or "advanced"

**Error Codes**:
- `400`: Missing TAVILY_API_KEY
- `404`: Thought ID doesn't exist
- `409`: Error during web enrichment

---

#### POST `/api/v1/thought_graph/enrich/web/batch`
Enrich multiple thoughts with web search in batch.

**Request Body**:
```json
{
  "thought_ids": ["thought_abc123", "thought_xyz789"],
  "max_results_per_thought": 3
}
```

**Response**: `List[WebEnrichmentResponseDTO]`

**Parameters**:
- `thought_ids` (required): List of thought IDs to enrich
- `max_results_per_thought` (optional, default: 3): Max results per thought (1-10)

**Error Codes**:
- `400`: Missing TAVILY_API_KEY
- `409`: Error during batch enrichment

---

### Project Matching

#### POST `/api/v1/thought_graph/projects/match`
Match thoughts to projects and repositories.

**Request Body**:
```json
{
  "project_patterns": {
    "cognee": ["cognee", "knowledge graph", "memory"],
    "backend-api": ["api", "server", "fastapi"]
  },
  "auto_detect_repos": true
}
```

**Response**: `ProjectMatchResponseDTO`
```json
{
  "project_matches": {
    "cognee": [
      {
        "thought_id": "thought_abc123",
        "confidence": 0.92,
        "matched_keywords": ["cognee", "knowledge graph"]
      }
    ],
    "backend-api": [
      {
        "thought_id": "thought_xyz789",
        "confidence": 0.85,
        "matched_keywords": ["api", "fastapi"]
      }
    ]
  },
  "total_matches": 2
}
```

**Parameters**:
- `project_patterns` (optional): Custom project pattern mappings
- `auto_detect_repos` (optional, default: true): Auto-detect GitHub/GitLab repos

**Error Codes**:
- `409`: Error during project matching

---

### Edge Weight Management

#### POST `/api/v1/thought_graph/edges/decay`
Decay edge weights based on time since last update.

**Request Body**:
```json
{
  "decay_rate": 0.1,
  "min_weight": 0.15,
  "days_threshold": 30
}
```

**Response**:
```json
{
  "edges_decayed": 15,
  "edges_removed": 3,
  "total_processed": 50
}
```

**Parameters**:
- `decay_rate` (optional, default: 0.1): Decay rate per day (0.0-1.0)
- `min_weight` (optional, default: 0.15): Minimum weight before removal (0.0-1.0)
- `days_threshold` (optional, default: 30): Days since last update for decay

**Error Codes**:
- `400`: Invalid parameters
- `409`: Error during edge decay

---

#### POST `/api/v1/thought_graph/edges/reinforce`
Reinforce a specific edge by increasing its weight.

**Request Body**:
```json
{
  "source_id": "thought_abc123",
  "target_id": "thought_xyz789",
  "reinforcement_amount": 0.1
}
```

**Response**:
```json
{
  "edge_reinforced": true,
  "new_weight": 0.85,
  "previous_weight": 0.75
}
```

**Parameters**:
- `source_id` (required): Source thought ID
- `target_id` (required): Target thought ID
- `reinforcement_amount` (optional, default: 0.1): Amount to increase weight (0.0-1.0)

**Error Codes**:
- `400`: Invalid parameters
- `404`: Edge doesn't exist
- `409`: Error during reinforcement

---

#### GET `/api/v1/thought_graph/edges/potential`
Calculate potential connections with weighted suggestions.

**Query Parameters**:
- `min_potential_score` (optional, default: 0.5): Minimum potential score
- `limit` (optional, default: 20): Maximum results

**Response**: `List[dict]`
```json
[
  {
    "source_id": "thought_abc123",
    "target_id": "thought_def456",
    "potential_score": 0.75,
    "reason": "High semantic similarity and tag overlap"
  }
]
```

**Error Codes**:
- `409`: Error calculating potential connections

---

### Integrated Memify

#### POST `/api/v1/thought_graph/memify`
Comprehensive thought graph enrichment in one command.

**Request Body**:
```json
{
  "enable_web_enrichment": true,
  "enable_project_matching": true,
  "enable_edge_decay": true,
  "enable_potential_connections": true,
  "project_patterns": {
    "cognee": ["cognee", "knowledge graph"]
  },
  "web_search_top_k": 5
}
```

**Response**:
```json
{
  "graph_enrichment": {
    "pagerank_scores": {...},
    "communities": {...}
  },
  "web_enrichment": {
    "thoughts_enriched": 5,
    "total_results": 25
  },
  "project_matching": {
    "total_matches": 10
  },
  "edge_management": {
    "edges_decayed": 15,
    "edges_removed": 3
  },
  "potential_connections": [...]
}
```

**Parameters**:
- `enable_web_enrichment` (optional, default: false): Enable web search (requires TAVILY_API_KEY)
- `enable_project_matching` (optional, default: true): Enable project matching
- `enable_edge_decay` (optional, default: true): Enable edge weight decay
- `enable_potential_connections` (optional, default: true): Calculate potential connections
- `project_patterns` (optional): Custom project patterns
- `web_search_top_k` (optional, default: 5): Top K thoughts to enrich with web

**Error Codes**:
- `409`: Error during memify operation

---

### Graph Exploration

#### GET `/api/v1/thought_graph/thoughts/{thought_id}/neighbors`
Get neighboring thoughts for a specific thought.

**Path Parameters**:
- `thought_id`: ID of the thought

**Query Parameters**:
- `max_hops` (optional, default: 1): Maximum hops from the thought

**Response**: `List[ThoughtResponseDTO]`

**Error Codes**:
- `404`: Thought ID doesn't exist
- `409`: Error getting neighbors

---

#### GET `/api/v1/thought_graph/communities`
Get thought communities detected in the graph.

**Response**:
```json
{
  "communities": {
    "0": ["thought_abc123", "thought_xyz789"],
    "1": ["thought_def456", "thought_ghi012"]
  },
  "total_communities": 2
}
```

**Error Codes**:
- `409`: Error getting communities

---

## Usage Examples

### Python Client Example

```python
import requests

# Configuration
BASE_URL = "http://localhost:8000/api/v1/thought_graph"
AUTH_TOKEN = "your_auth_token"
headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}

# Add a thought
response = requests.post(
    f"{BASE_URL}/thoughts",
    json={
        "content": "Build graph database for ADHD thought management",
        "tags": ["adhd", "productivity"],
        "importance_score": 9,
        "auto_connect": True
    },
    headers=headers
)
thought = response.json()
print(f"Created thought: {thought['id']}")

# Discover connections
response = requests.post(
    f"{BASE_URL}/connections/discover",
    json={
        "thought_id": thought["id"],
        "similarity_threshold": 0.7
    },
    headers=headers
)
connections = response.json()
print(f"Found {len(connections)} connections")

# Enrich graph
response = requests.post(
    f"{BASE_URL}/enrich",
    json={
        "compute_pagerank": True,
        "detect_communities": True
    },
    headers=headers
)
enrichment = response.json()
print(f"Graph enriched in {enrichment['processing_time']}s")

# Run integrated memify
response = requests.post(
    f"{BASE_URL}/memify",
    json={
        "enable_web_enrichment": True,
        "enable_project_matching": True,
        "enable_edge_decay": True,
        "project_patterns": {
            "cognee": ["cognee", "knowledge graph"]
        }
    },
    headers=headers
)
results = response.json()
print(f"Memify complete: {results}")
```

### cURL Examples

```bash
# Add a thought
curl -X POST "http://localhost:8000/api/v1/thought_graph/thoughts" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Build graph database for ADHD",
    "tags": ["adhd", "productivity"],
    "importance_score": 9
  }'

# Enrich graph
curl -X POST "http://localhost:8000/api/v1/thought_graph/enrich" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "compute_pagerank": true,
    "detect_communities": true
  }'

# Get surprise connections
curl -X GET "http://localhost:8000/api/v1/thought_graph/connections/surprise?min_surprise_score=0.6&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Run memify
curl -X POST "http://localhost:8000/api/v1/thought_graph/memify" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "enable_web_enrichment": true,
    "enable_project_matching": true,
    "enable_edge_decay": true
  }'
```

---

## Configuration

### Environment Variables

- `TAVILY_API_KEY` (optional): Required for web enrichment features
- `THOUGHT_GRAPH_DECAY_RATE` (optional): Default decay rate (default: 0.1)
- `THOUGHT_GRAPH_MIN_WEIGHT` (optional): Minimum edge weight (default: 0.15)
- `THOUGHT_GRAPH_DAYS_THRESHOLD` (optional): Days threshold for decay (default: 30)

### Authentication

All endpoints require authentication using the same mechanism as other Cognee API endpoints:
- **Bearer Token**: Include `Authorization: Bearer <token>` header
- **Cookie**: Use session cookie (for web clients)

---

## Implementation Status

### Fully Implemented (Production-Ready)
- ✅ Thought management (add, batch add)
- ✅ Connection discovery (semantic, tag-based)
- ✅ Graph enrichment (PageRank, centrality, communities, transitive)
- ✅ Surprise connection finding
- ✅ Graph exploration (neighbors, communities)
- ✅ Input validation throughout
- ✅ Error handling with descriptive messages

### Partially Implemented (With Documented Limitations)
- ⚠️ Web enrichment (75%): API integration complete, retrieves and logs results; graph persistence pending WebResource model
- ⚠️ Project matching (80%): Analysis complete, reports matches; node property updates pending backend support
- ⚠️ Edge weight management (60%): Calculation complete, reports changes; edge property updates pending backend support

### Backend Dependencies for Full Functionality
1. Graph backend edge property update support
2. Graph backend node property update support
3. WebResource data model creation
4. Transaction support for atomic operations

See `cognee/modules/thought_graph/IMPLEMENTATION_STATUS.md` for complete details.

---

## Best Practices

### Thought Capture
- Use descriptive content that captures the essence of the idea
- Add relevant tags for easier categorization
- Set energy_level to track mental state when idea occurred
- Set importance_score to prioritize thoughts
- Enable auto_connect for automatic relationship discovery

### Graph Enrichment
- Run enrichment periodically (e.g., daily or weekly)
- Use auto_add_transitive_links sparingly to avoid graph bloat
- Review surprise connections for serendipitous insights

### Web Enrichment
- Use for important thoughts that benefit from external context
- Set appropriate max_results to balance detail and cost
- Use "basic" search_depth for most cases, "advanced" for complex topics

### Project Matching
- Define clear project patterns based on your workflow
- Enable auto_detect_repos to catch repository mentions
- Review matches periodically to refine patterns

### Edge Management
- Run decay regularly to keep graph relevant
- Reinforce important connections to prevent pruning
- Review potential connections for insights

### Integrated Memify
- Use as primary enrichment command for comprehensive results
- Enable web_enrichment selectively (costs API calls)
- Customize project_patterns for your projects
- Run on a schedule for automated maintenance

---

## Error Handling

All endpoints use consistent error response format:

```json
{
  "error": "Detailed error message explaining what went wrong"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `404`: Not Found (resource doesn't exist)
- `409`: Conflict (error during operation)
- `500`: Internal Server Error (unexpected error)

---

## Support

For issues, questions, or feature requests related to the Thought Graph API:
- GitHub Issues: https://github.com/topoteretes/cognee/issues
- Discord: https://discord.gg/NQPKmU5CCg
- Email: vasilije@cognee.ai

---

## License

Apache 2.0 - See LICENSE file for details.
