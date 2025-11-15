# Enhanced Thought Graph Features - Implementation Summary

## Overview

This document summarizes the new advanced features added to the thought graph system based on feedback for enriching braindumps with web searches, project matching, and edge weight management.

## New Features Implemented

### 1. Web Enrichment (Memify Integration)

**Purpose**: Enrich thoughts with external knowledge from the web

**New Operations:**
- `enrich_with_web_search()` - Search web using Tavily API
- `enrich_with_scraped_content()` - Scrape specific URLs
- `batch_enrich_with_web()` - Efficiently enrich multiple thoughts

**Usage:**
```python
from cognee.modules.thought_graph.operations import enrich_with_web_search

# Enrich a thought with web research
results = await enrich_with_web_search(
    thought_id=thought.id,
    max_results=5,
    search_depth="advanced",  # "basic" or "advanced"
    use_tavily=True
)

# Returns:
# - search_results: List of web resources found
# - connections_created: Number of new connections
# - content_added: Amount of content retrieved
```

**Configuration:**
- Requires `TAVILY_API_KEY` environment variable
- Supports both "basic" and "advanced" search depths
- Configurable result limits

**Use Cases:**
- Research assistance
- Fact checking
- Context enrichment
- Discovery of related concepts

### 2. Project & Repository Matching

**Purpose**: Automatically match thoughts to projects and code repositories

**New Operations:**
- `match_to_projects()` - Match thoughts to projects
- `create_project_connections()` - Create project links
- `find_project_clusters()` - Find project-based clusters

**Usage:**
```python
from cognee.modules.thought_graph.operations import match_to_projects

# Match thoughts to projects
results = await match_to_projects(
    auto_detect=True,  # Auto-detect GitHub/GitLab repos
    project_patterns={
        "cognee": ["cognee", "knowledge graph", "memory"],
        "backend-api": ["api", "server", "backend"]
    }
)

# Returns:
# - thoughts_matched: Number of thoughts matched
# - projects_found: Set of project names
# - matches: List of (thought_id, project, confidence)
```

**Features:**
- Auto-detects GitHub/GitLab repository URLs
- Custom pattern matching
- Confidence scoring (0.0-1.0)
- Updates ThoughtNode.related_projects field

**Use Cases:**
- Project management
- Code repository tracking
- Work organization
- Context switching support

### 3. Edge Weight Management

**Purpose**: Maintain graph health with automatic decay and reinforcement

**New Operations:**
- `decay_edge_weights()` - Apply time-based decay
- `reinforce_edge()` - Strengthen connections
- `calculate_potential_connections()` - Find missing links
- `prune_weak_connections()` - Remove stale edges

**Usage:**
```python
from cognee.modules.thought_graph.operations import (
    decay_edge_weights,
    reinforce_edge,
    calculate_potential_connections
)

# Apply decay to old connections
decay_results = await decay_edge_weights(
    decay_rate=0.1,         # 10% reduction
    min_weight=0.15,        # Remove below this threshold
    time_based=True,        # Decay based on age
    days_threshold=30       # Full decay after 30 days
)

# Reinforce an important connection
await reinforce_edge(
    source_id=thought1.id,
    target_id=thought2.id,
    reinforcement_amount=0.2
)

# Find potential new connections
potentials = await calculate_potential_connections(
    thought_id=thought.id,
    min_potential_weight=0.4,
    max_results=10
)
```

**Decay Mechanics:**
- Weights gradually reduce over time
- Edges removed when weight drops below threshold (configurable, default ~0.1)
- Recent connections preserved even if weak
- Time-based graduated decay

**Reinforcement:**
- Connections strengthened when actively used
- Maximum weight cap (1.0)
- Manual or automatic reinforcement

**Potential Connections:**
- Calculates likelihood of missing connections
- Based on:
  - Shared community membership
  - Common neighbors
  - Tag similarity
  - Project overlap
- Returns weighted suggestions

### 4. Enhanced Memify Pipeline

**Purpose**: Integrated enrichment combining all features

**New Operation:**
- `memify_thoughts()` - Complete enrichment pipeline
- `cognify_and_memify_thoughts()` - Combined processing

**Usage:**
```python
from cognee.modules.thought_graph.operations import memify_thoughts

# Full enrichment pipeline
results = await memify_thoughts(
    thought_ids=None,  # None = all thoughts
    enable_web_enrichment=True,
    enable_project_matching=True,
    enable_edge_decay=True,
    enable_potential_connections=True,
    web_search_depth="basic",
    max_web_results=3,
    decay_rate=0.1,
    min_edge_weight=0.1,
    project_patterns={
        "my_project": ["keyword1", "keyword2"]
    }
)

# Returns comprehensive results:
# - graph_enrichment: PageRank, communities, etc.
# - web_enrichment: Search results and connections
# - project_matching: Project associations
# - edge_management: Decay and removal stats
# - potential_connections: New connection suggestions
```

**Pipeline Phases:**
1. **Graph Algorithm Enrichment** - PageRank, centrality, communities, transitive
2. **Web Enrichment** - Search and scraping (if enabled)
3. **Project Matching** - Auto-detect and pattern matching
4. **Edge Weight Management** - Decay and pruning
5. **Potential Connections** - Discovery of missing links

**Recommended Schedule:**
- **After adding thoughts**: Run immediately with `enable_web_enrichment=True`
- **Daily**: For active projects
- **Weekly**: Regular maintenance
- **Monthly**: Deep cleanup with higher decay rate

## Integration with Cognify

The memify operations integrate seamlessly with cognify:

```python
# After cognify, run memify
await cognee.cognify()
await memify_thoughts(
    enable_web_enrichment=True,
    enable_project_matching=True
)
```

Or use the combined operation:

```python
from cognee.modules.thought_graph.operations import cognify_and_memify_thoughts

# Process data and enrich in one call
results = await cognify_and_memify_thoughts(
    data=my_data,
    enable_all_enrichments=True,
    project_patterns=PROJECT_PATTERNS
)
```

## Configuration

### Environment Variables

```bash
# Required for web enrichment
TAVILY_API_KEY=your_tavily_api_key

# Optional: Customize decay behavior
THOUGHT_GRAPH_DECAY_RATE=0.1
THOUGHT_GRAPH_MIN_WEIGHT=0.15
THOUGHT_GRAPH_DAYS_THRESHOLD=30
```

### Project Patterns

Create reusable project patterns:

```python
PROJECT_PATTERNS = {
    "cognee": [
        "cognee",
        "knowledge graph",
        "thought graph",
        "memory system"
    ],
    "research": [
        "paper",
        "study",
        "research",
        "publication"
    ],
    "backend": [
        "api",
        "server",
        "backend",
        "database"
    ]
}
```

## Use Cases

### 1. Research Project with Web Enrichment

```python
# Capture research notes
thoughts = await add_thoughts_batch([
    {"content": "Graph neural networks for knowledge graphs", 
     "tags": ["research", "gnn"]},
    {"content": "ADHD and working memory limitations",
     "tags": ["research", "adhd", "neuroscience"]}
])

# Enrich each with web research
for thought in thoughts:
    await enrich_with_web_search(
        thought_id=thought.id,
        search_depth="advanced",
        max_results=5
    )

# Run full enrichment
results = await memify_thoughts()
```

### 2. Project-Based Organization

```python
# Match all thoughts to projects
results = await match_to_projects(
    project_patterns={
        "project_alpha": ["alpha", "feature-a", "backend"],
        "project_beta": ["beta", "frontend", "ui"],
        "research": ["paper", "study", "academic"]
    }
)

# Find all thoughts for a specific project
clusters = await find_project_clusters()
alpha_thoughts = clusters.get("project_alpha", [])
```

### 3. Weekly Knowledge Maintenance

```python
# Weekly graph cleanup
decay_results = await decay_edge_weights(
    decay_rate=0.15,        # Higher decay for cleanup
    min_weight=0.2,         # Higher threshold
    time_based=True
)

# Find and review potential connections
for thought_id in recently_active_thoughts:
    potentials = await calculate_potential_connections(
        thought_id=thought_id,
        min_potential_weight=0.5
    )
    # Review and manually create valuable connections
```

### 4. Discovery Workflow

```python
# Find surprise connections
surprises = await find_surprise_connections(min_surprise_score=0.6)

# Enrich surprising connections with web context
for surprise in surprises[:5]:
    await enrich_with_web_search(surprise.source_id)
    await enrich_with_web_search(surprise.target_id)

# Run full enrichment to update metrics
await memify_thoughts()
```

## Architecture

### Data Flow

```
Input: Braindump / Thoughts
    ↓
Add Thoughts (capture)
    ↓
Auto-Connect (semantic + tags)
    ↓
Graph Enrichment (PageRank, communities, transitive)
    ↓
Web Enrichment (Tavily search + scraping) ←──────┐
    ↓                                             │
Project Matching (auto-detect + patterns)        │
    ↓                                             │
Edge Decay (time-based weight reduction)         │
    ↓                                             │
Potential Connections (missing link discovery)   │
    ↓                                             │
Memify Pipeline ──────────────────────────────────┘
    ↓
Output: Enriched Knowledge Graph
```

### Integration Points

- **Tavily API**: Web search and research
- **Web Scraper**: Content extraction from URLs
- **Vector Search**: Semantic similarity
- **Graph Database**: Node and edge storage
- **LLM**: Future connection inference

## Performance Considerations

### Web Enrichment

- API rate limits apply (Tavily)
- Batch operations for efficiency
- Configurable result limits
- Cache search results to avoid duplicates

### Edge Decay

- O(E) complexity where E = number of edges
- Run periodically, not on every operation
- Configurable thresholds for performance

### Project Matching

- O(N) complexity where N = number of thoughts
- Regex patterns compiled once
- Results cached per session

### Potential Connections

- O(N²) in worst case
- Limited to specific thoughts or top N
- Uses graph structure for optimization

## Best Practices

### 1. Gradual Enrichment

Start with basic enrichment, add web/project features as needed:

```python
# Basic enrichment
await enrich_thought_graph()

# Add web enrichment for important thoughts
for thought in high_priority_thoughts:
    await enrich_with_web_search(thought.id)

# Full enrichment periodically
await memify_thoughts(enable_all=True)
```

### 2. Project Pattern Evolution

Start simple, refine patterns based on results:

```python
# Initial patterns
patterns_v1 = {
    "cognee": ["cognee"]
}

# Refined after reviewing matches
patterns_v2 = {
    "cognee": ["cognee", "knowledge graph", "thought graph", "memory"]
}
```

### 3. Decay Tuning

Adjust decay parameters based on graph behavior:

```python
# Conservative (slow decay)
await decay_edge_weights(decay_rate=0.05, min_weight=0.1)

# Aggressive (fast cleanup)
await decay_edge_weights(decay_rate=0.2, min_weight=0.3)

# Balanced (recommended)
await decay_edge_weights(decay_rate=0.1, min_weight=0.15)
```

### 4. Scheduled Maintenance

Set up regular enrichment schedule:

```python
# Daily: Light enrichment
await memify_thoughts(
    enable_web_enrichment=False,
    enable_edge_decay=True,
    decay_rate=0.05
)

# Weekly: Full enrichment
await memify_thoughts(
    enable_web_enrichment=True,
    enable_all=True,
    decay_rate=0.1
)

# Monthly: Deep cleanup
await memify_thoughts(
    enable_all=True,
    decay_rate=0.2,
    min_edge_weight=0.25
)
```

## Troubleshooting

### Web Enrichment Not Working

- Check `TAVILY_API_KEY` is set
- Verify API quota/limits
- Check network connectivity
- Review logs for specific errors

### Project Matching Too Broad/Narrow

- Refine project patterns
- Adjust confidence thresholds
- Use more specific keywords
- Check for regex pattern issues

### Too Many/Few Connections Removed

- Adjust `decay_rate` parameter
- Change `min_weight` threshold
- Modify `days_threshold` for time-based decay
- Use `preserve_recent=True`

### Performance Issues

- Limit `thought_ids` to specific subset
- Reduce `max_web_results`
- Disable expensive features temporarily
- Run enrichment less frequently

## Future Enhancements

- **LLM-based connection inference**: Use LLMs to discover non-obvious connections
- **Collaborative filtering**: Learn from user interactions
- **Temporal analysis**: Track thought evolution over time
- **Multi-modal enrichment**: Images, audio, video
- **Real-time enrichment**: Stream-based processing
- **Advanced caching**: Reduce API calls

## Summary

The enhanced thought graph system now provides:

✅ **Web Enrichment**: Deep research and context from the web
✅ **Project Matching**: Automatic project and repository tracking
✅ **Edge Weight Management**: Organic graph evolution with decay/reinforcement
✅ **Potential Connections**: Discovery of missing links
✅ **Integrated Pipeline**: One-command full enrichment
✅ **ADHD Optimization**: Low-friction workflows

All features are production-ready, well-documented, and tested.
