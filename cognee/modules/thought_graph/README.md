# Thought Graph Module

An ADHD-optimized system for managing scattered thoughts, discovering hidden connections, and organizing brainfog into actionable insights.

## Overview

The Thought Graph module helps you:
- **Quickly capture** thoughts and ideas without breaking flow
- **Automatically discover** connections between related ideas
- **Find hidden patterns** through graph algorithms (PageRank, community detection)
- **Surface surprise connections** that spark creative insights
- **Organize chaos** into thematic clusters

## Key Features

### 1. Quick Thought Capture
```python
from cognee.modules.thought_graph.operations import add_thought

# Capture a thought instantly
thought = await add_thought(
    content="Build a knowledge graph for ADHD thought management",
    tags=["adhd", "productivity", "ideas"],
    importance_score=8,
    auto_connect=True  # Automatically find related thoughts
)
```

### 2. Automatic Connection Discovery
The system uses multiple methods to discover connections:
- **Semantic similarity**: Vector embeddings find content-related thoughts
- **Tag overlap**: Shared categorization suggests relationships
- **LLM inference**: AI discovers non-obvious connections

### 3. Graph Enrichment Algorithms

#### PageRank: Find Influential Thoughts
```python
from cognee.modules.thought_graph.operations import enrich_thought_graph

results = await enrich_thought_graph(
    compute_pagerank=True,
    detect_communities_flag=True,
    find_transitive=True
)
```

PageRank identifies which thoughts are most "important" based on how they connect to other important thoughts.

#### Centrality: Find Bridge Ideas
Centrality measures identify thoughts that connect different topic clusters - the "bridge" ideas that tie your thinking together.

#### Community Detection: Organize Into Clusters
Automatically groups related thoughts into thematic communities, helping you see how your scattered ideas naturally organize.

#### Transitive Connections: Find Hidden Links
Discovers indirect relationships (A -> B -> C) that reveal non-obvious connections between your thoughts.

### 4. Surprise Connections
```python
from cognee.modules.thought_graph.operations import find_surprise_connections

surprises = await find_surprise_connections(
    min_surprise_score=0.5,
    max_results=20
)

for surprise in surprises:
    print(f"{surprise.explanation}")
    print(f"Score: {surprise.overall_score:.2f}")
```

Finds unexpected connections based on:
- **Semantic distance**: Very different content/topics
- **Temporal distance**: Ideas captured far apart in time
- **Structural distance**: Far apart in the graph
- **Domain distance**: Different categories/tags

### 5. Neighborhood Exploration
```python
from cognee.modules.thought_graph.operations import get_thought_neighbors

neighbors = await get_thought_neighbors(
    thought_id=your_thought_id,
    max_depth=2  # Get neighbors of neighbors
)
```

## Why This Helps ADHD Brains

### Non-Linear Thinking
ADHD brains naturally think in associative, non-linear patterns. The thought graph embraces this by:
- Allowing ideas to connect in any direction
- Not forcing hierarchical organization
- Revealing unexpected associations

### Working Memory Support
Instead of trying to hold multiple thoughts in working memory, externalize them:
- Quick capture prevents ideas from being lost
- Graph maintains relationships automatically
- Visual representation reduces cognitive load

### Serendipitous Discovery
ADHD brains excel at making creative connections. The surprise connection finder:
- Surfaces non-obvious relationships
- Highlights distant but related ideas
- Sparks new insights through unexpected associations

### Reduced Organization Overhead
Traditional note-taking requires upfront organization decisions. This system:
- Captures first, organizes later
- Uses algorithms to find natural structure
- Grows smarter as you add more thoughts

## Complete Example

See `examples/python/thought_graph_example.py` for a comprehensive demonstration:

```bash
python examples/python/thought_graph_example.py
```

## Models

### ThoughtNode
Represents a single thought/idea with metadata:
- `content`: The thought content (text)
- `title`: Optional short title
- `tags`: List of categorization tags
- `importance_score`: User-defined importance (1-10)
- `energy_level`: Energy when captured (useful for ADHD patterns)
- `pagerank_score`: Computed influence score
- `centrality_score`: Computed bridge score
- `community_id`: Thematic cluster ID

### Connection
Represents a relationship between thoughts:
- `source_id`, `target_id`: Connected thought IDs
- `relationship_type`: Type of relationship
- `strength`: Connection strength (0.0-1.0)
- `discovery_method`: How it was found
- `surprise_score`: How unexpected it is

### SurpriseScore
Quantifies unexpectedness of a connection:
- `overall_score`: Combined surprise measure
- `semantic_distance`: Content dissimilarity
- `temporal_distance`: Time separation
- `structural_distance`: Graph distance
- `domain_distance`: Category dissimilarity

## Algorithms

### PageRank
Identifies influential thoughts based on the "prestige" of their connections. Thoughts referenced by other important thoughts get higher scores.

**Use cases:**
- Find foundational ideas in your thinking
- Identify hub concepts that connect topics
- Prioritize which thoughts to develop further

### Centrality Measures
- **Betweenness**: Thoughts that lie on paths between others (bridges)
- **Closeness**: Thoughts close to all others (central concepts)
- **Degree**: Thoughts with many direct connections
- **Eigenvector**: Thoughts connected to other important thoughts

**Use cases:**
- Find bridge ideas connecting different domains
- Identify well-connected "hub" thoughts
- Discover central themes in your thinking

### Community Detection
Groups thoughts into clusters based on connectivity patterns using:
- **Greedy modularity**: Fast, good quality
- **Label propagation**: Very fast for large graphs

**Use cases:**
- Organize scattered thoughts into themes
- Discover natural topic groupings
- Identify isolated thoughts needing connections

### Transitive Connections
Finds indirect relationships (A->B->C) that could become direct connections (A->C).

**Use cases:**
- Discover hidden relationships
- Strengthen the graph with implicit connections
- Find chains of reasoning

## Integration with Cognee

The thought graph module integrates seamlessly with Cognee's existing features:

- **Vector search**: Uses Cognee's vector engine for semantic similarity
- **Graph database**: Stores thoughts in Cognee's graph infrastructure
- **LLM integration**: Can use Cognee's LLM gateway for inference
- **Visualization**: Compatible with Cognee's graph visualization

## Best Practices

### 1. Capture Often
Add thoughts as they occur - don't worry about organization. Let the algorithms find patterns.

### 2. Use Tags Loosely
Tags help categorization but don't over-think them. The system discovers connections beyond tags.

### 3. Enrich Periodically
Run `enrich_thought_graph()` after adding multiple thoughts to update metrics and find new connections.

### 4. Explore Surprises
Review surprise connections regularly - they often spark the most creative insights.

### 5. Follow the Graph
Use neighborhood exploration to "walk" through your thoughts, following connections to related ideas.

## Future Enhancements

- **Temporal patterns**: Analyze how your thinking evolves over time
- **Energy-aware suggestions**: Recommend thoughts to work on based on current energy level
- **Interactive visualization**: Web-based graph explorer
- **Voice capture**: Add thoughts via speech
- **Cross-project links**: Connect thoughts to tasks and projects
- **Collaborative graphs**: Share and merge thought networks

## Technical Details

**Dependencies:**
- NetworkX: Graph algorithms
- Cognee infrastructure: Vector search, graph database, LLM

**Performance:**
- Optimized for graphs with 100-10,000 thoughts
- Community detection scales to larger graphs
- Transitive connection finding limited to prevent exponential growth

**Storage:**
- Thoughts stored as DataPoint nodes in Cognee's graph database
- Connections stored as graph edges
- Computed metrics stored as node properties

## References

**Research Foundations:**
- PageRank: Brin & Page (1998)
- Community Detection: Newman (2004), Louvain method
- ADHD Knowledge Management: Research on external memory systems
- PKM Systems: Obsidian, Roam Research, Zettelkasten method

**ADHD-Specific Design:**
- Non-linear thinking accommodation
- Working memory externalization
- Reduced organizational overhead
- Serendipitous discovery support

## Advanced Features

### Web Enrichment

Enrich thoughts with web search results and scraped content:

```python
from cognee.modules.thought_graph.operations import enrich_with_web_search

# Enrich a thought with web search
results = await enrich_with_web_search(
    thought_id=thought.id,
    max_results=5,
    search_depth="advanced",  # or "basic"
    use_tavily=True
)

# Results include:
# - search_results: List of relevant web resources
# - connections_created: New connections to web content
# - content_added: Amount of new content
```

**Use Cases:**
- Research assistance: Pull in external knowledge
- Context enrichment: Add relevant background information
- Fact checking: Find supporting or contradicting sources
- Discovery: Uncover related concepts and ideas

**Requirements:** Set `TAVILY_API_KEY` environment variable for web search

### Project Matching

Automatically match thoughts to projects and repositories:

```python
from cognee.modules.thought_graph.operations import match_to_projects

# Match thoughts to projects
results = await match_to_projects(
    auto_detect=True,  # Auto-detect repo URLs
    project_patterns={
        "cognee": ["cognee", "knowledge graph", "memory"],
        "backend-api": ["api", "server", "backend"]
    }
)

# Results include:
# - thoughts_matched: Number of thoughts matched
# - projects_found: Set of project names
# - matches: List of (thought_id, project, confidence)
```

**Use Cases:**
- Project organization: Group thoughts by project
- Repository tracking: Link ideas to code repositories
- Work planning: See all thoughts related to a project
- Context switching: Find project-specific ideas

### Edge Weight Management

Manage connection strength with decay and reinforcement:

```python
from cognee.modules.thought_graph.operations import (
    decay_edge_weights,
    reinforce_edge,
    calculate_potential_connections
)

# Apply time-based decay
decay_results = await decay_edge_weights(
    decay_rate=0.1,        # 10% reduction
    min_weight=0.15,       # Remove below this
    time_based=True,       # Decay old edges more
    days_threshold=30      # Full decay after 30 days
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

**Use Cases:**
- Graph maintenance: Keep connections relevant
- Organic evolution: Let graph adapt over time
- Quality control: Remove noise and weak connections
- Discovery: Find missing links

**Edge Weight Factors:**
- Time: Older connections decay faster
- Usage: Reinforced when actively used
- Relevance: Maintained by algorithms
- User feedback: Manually adjusted

### Enhanced Memify

Integrated enrichment pipeline combining all features:

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

**Recommended Schedule:**
- After adding thoughts: Run immediately
- Daily: For active projects
- Weekly: For maintenance
- Monthly: Deep cleanup with higher decay

## Use Cases

### 1. Research Projects
```python
# Capture research notes
thoughts = await add_thoughts_batch([
    {"content": "Paper on graph neural networks", "tags": ["research", "gnn"]},
    {"content": "ADHD and working memory limitations", "tags": ["research", "adhd"]}
])

# Enrich with web research
for thought in thoughts:
    await enrich_with_web_search(thought.id, search_depth="advanced")

# Run full enrichment
await memify_thoughts()
```

### 2. Project Management
```python
# Match existing thoughts to projects
results = await match_to_projects(
    project_patterns={
        "project_alpha": ["alpha", "feature-a", "backend"],
        "project_beta": ["beta", "frontend", "ui"]
    }
)

# Find all thoughts for a project
clusters = await find_project_clusters()
project_thoughts = clusters.get("project_alpha", [])
```

### 3. Knowledge Maintenance
```python
# Weekly cleanup
decay_results = await decay_edge_weights(
    decay_rate=0.15,
    min_weight=0.2,
    time_based=True
)

# Find and create missing connections
for thought_id in active_thoughts:
    potentials = await calculate_potential_connections(thought_id)
    # Review and create valuable connections
```

### 4. Discovery & Serendipity
```python
# Find surprise connections
surprises = await find_surprise_connections(min_surprise_score=0.6)

# Get web context for interesting ideas
for surprise in surprises[:5]:
    await enrich_with_web_search(surprise.source_id)
    await enrich_with_web_search(surprise.target_id)
```

## Configuration

### Environment Variables

```bash
# Required for web enrichment
TAVILY_API_KEY=your_tavily_api_key

# Optional: Customize decay behavior
THOUGHT_GRAPH_DECAY_RATE=0.1
THOUGHT_GRAPH_MIN_WEIGHT=0.15
```

### Project Patterns

Define reusable project patterns:

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
    "personal": [
        "life",
        "personal",
        "self-improvement"
    ]
}

# Use in operations
await match_to_projects(project_patterns=PROJECT_PATTERNS)
await memify_thoughts(project_patterns=PROJECT_PATTERNS)
```

## Architecture

### Data Flow

```
Thoughts → Add/Capture
    ↓
Auto-Connect (semantic + tags)
    ↓
Enrich (PageRank, communities, transitive)
    ↓
Web Enrich (search + scrape) ←─────┐
    ↓                               │
Project Match (auto-detect)         │
    ↓                               │
Edge Decay (time-based)             │
    ↓                               │
Potential Connections               │
    ↓                               │
Memify Pipeline ────────────────────┘
    ↓
Enriched Knowledge Graph
```

### Integration Points

- **Vector Search**: Semantic similarity matching
- **Graph Database**: Node and edge storage
- **Web Search**: Tavily API integration
- **LLM**: Future connection inference
- **Project Systems**: GitHub, GitLab integration

