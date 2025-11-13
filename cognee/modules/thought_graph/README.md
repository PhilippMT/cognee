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
