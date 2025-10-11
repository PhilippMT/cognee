# HelixDB Hybrid Adapter for Cognee

A hybrid graph-vector database adapter for HelixDB, providing unified access to both graph and vector operations within the cognee framework.

## Overview

HelixDB is a high-performance database built in Rust, designed specifically for AI applications. It combines graph and vector capabilities in a single platform with ultra-low latency.

This adapter integrates HelixDB into cognee, implementing both `GraphDBInterface` and `VectorDBInterface` for seamless hybrid operations.

## Installation

### Prerequisites

1. **Install HelixDB CLI**:
```bash
curl -fsSL "https://install.helix-db.com" | bash
```

2. **Install helix-py Python SDK**:
```bash
pip install helix-py
```

3. **Setup HelixDB Project**:
```bash
helix install
helix setup
```

This creates a HelixDB configuration directory with `.hx` schema files.

## Configuration

### Basic Setup

```python
from cognee.infrastructure.databases.hybrid.helixdb import HelixDBAdapter
from cognee.infrastructure.databases.vector.embeddings import get_embedding_engine

# Get embedding engine
embedding_engine = get_embedding_engine()

# Initialize adapter
adapter = HelixDBAdapter(
    config_path="./helixdb-cfg",  # Path to your HelixDB config
    port=6969,                     # Default HelixDB port
    local=True,                    # Use local instance
    embedding_engine=embedding_engine,
    auto_start=True                # Auto-start local instance
)
```

### Cloud/Remote Setup

```python
adapter = HelixDBAdapter(
    config_path="./helixdb-cfg",
    api_endpoint="https://your-helix-instance.com",
    local=False,
    embedding_engine=embedding_engine
)
```

## Schema Management

HelixDB requires schema definitions in `.hx` files. Here's an example schema:

```helix
# In your helixdb-cfg/schema.hx file

NODE User {
    name: String,
    age: I64,
    embedding: Vec<F64>
}

NODE Document {
    content: String,
    embedding: Vec<F64>
}

EDGE FOLLOWS {
    User -> User
}

EDGE CONTAINS {
    Document -> User
}
```

### Compile Schema

```bash
cd helixdb-cfg
helix check
helix deploy
```

## Usage Examples

### Vector Operations

```python
from cognee.infrastructure.engine import DataPoint

# Create collection
await adapter.create_collection("my_documents")

# Create data points with embeddings
class MyDocument(DataPoint):
    text: str
    metadata: dict = {"index_fields": ["text"]}

documents = [
    MyDocument(id="doc1", text="First document"),
    MyDocument(id="doc2", text="Second document"),
]

# Insert documents with automatic embedding
await adapter.create_data_points("my_documents", documents)

# Vector search
results = await adapter.search(
    collection_name="my_documents",
    query_text="search query",
    limit=5
)

# Retrieve specific documents
docs = await adapter.retrieve(
    collection_name="my_documents",
    data_point_ids=["doc1", "doc2"]
)
```

### Graph Operations

```python
from cognee.modules.engine.models import Entity

# Add nodes
entity1 = Entity(
    name="Python",
    description="Programming language"
)
entity2 = Entity(
    name="Rust",
    description="Systems programming language"
)

await adapter.add_nodes([entity1, entity2])

# Add edges
await adapter.add_edge(
    source_id=str(entity1.id),
    target_id=str(entity2.id),
    relationship_name="SIMILAR_TO",
    properties={"confidence": 0.8}
)

# Query nodes
node = await adapter.get_node(str(entity1.id))

# Get neighbors
neighbors = await adapter.get_neighbors(str(entity1.id))

# Get all connections
connections = await adapter.get_connections(str(entity1.id))
```

### Hybrid Operations

```python
# Add nodes with vectors
from cognee.modules.chunking.models import DocumentChunk

chunk = DocumentChunk(
    text="This is a document chunk about Python programming",
    chunk_size=50,
    chunk_index=0
)

# Add as graph node
await adapter.add_node(chunk)

# Also add as vector for similarity search
await adapter.create_data_points("chunks", [chunk])

# Now you can:
# 1. Traverse graph relationships
edges = await adapter.get_edges(str(chunk.id))

# 2. Perform vector similarity search
similar = await adapter.search(
    collection_name="chunks",
    query_text="Python programming",
    limit=5
)
```

### Custom HelixQL Queries

For advanced operations, you can define custom HelixQL queries:

```helix
# In your helixdb-cfg/queries.hx file

QUERY findUsersByAge(min_age: I64, max_age: I64) =>
    users <- N<User::WHERE(
        _::{age}::GTE(min_age),
        _::{age}::LTE(max_age)
    )>
    RETURN users

QUERY similarDocuments(query_vec: Vec<F64>, topk: I64) =>
    docs <- VecSearch<Document>(
        query_vec,
        topk: topk
    )
    RETURN docs
```

Then use them:

```python
# Execute custom query
results = await adapter.query(
    "findUsersByAge",
    {"min_age": 20, "max_age": 30}
)
```

## Important Limitations

### 🚨 Critical Limitations

1. **Query Pre-compilation Required**: All queries must be pre-compiled in `.hx` files and deployed before use. Dynamic query generation is not supported.

2. **No Native Collections**: Collections are implemented via node labels, not as first-class concepts. This may impact performance for some operations.

3. **No Partial Updates**: Node updates require full node replacement. Cannot update individual properties without rewriting the entire node.

4. **Schema Pre-definition**: Schema must be defined upfront in `.hx` files. Schema evolution requires redeployment.

5. **Fixed Embedding Dimensions**: Vector dimensions are fixed at schema creation time and cannot be changed without schema migration.

### ⚠️ Performance Limitations

- **Bulk Operations**: No native bulk insert/update APIs. Adapter implements batching using `asyncio.gather`.
- **Large Graphs**: `get_graph_data()` may be slow for very large graphs.
- **HNSW Indexing**: Vector search uses HNSW algorithm which may require tuning for optimal performance.

### 🔧 Operational Limitations

- **Instance Required**: Requires running HelixDB instance (local or remote).
- **CLI Dependency**: Requires HelixDB CLI for schema compilation and deployment.
- **Resource Usage**: LMDB storage may consume significant disk space.
- **SDK Maturity**: helix-py is relatively new (v0.2.30) - pin version for stability.

### 🔐 Security Limitations

- **Query Injection**: Parameterize all queries to avoid injection attacks.
- **Access Control**: Limited fine-grained permissions - implement at application layer.
- **Encryption**: No native at-rest encryption - use OS/disk-level encryption.

See [ANALYSIS.md](./ANALYSIS.md) for complete limitation details and mitigations.

## Best Practices

### 1. Schema Design

```helix
# Define clear, typed schemas
NODE DataPoint {
    id: String,
    content: String,
    embedding: Vec<F64>,  # Specify dimension in comments: e.g., 1536 for OpenAI
    metadata: String      # Store JSON as string
}

# Index frequently accessed properties
# (Note: HelixDB handles indexing automatically)
```

### 2. Query Organization

```helix
# Group related queries in separate files
# queries/users.hx
QUERY addUser(name: String, age: I64) => ...
QUERY getUser(id: String) => ...

# queries/search.hx
QUERY vectorSearch(query_vec: Vec<F64>, topk: I64) => ...
```

### 3. Error Handling

```python
try:
    await adapter.add_node(entity)
except RuntimeError as e:
    if "not found" in str(e):
        # Query not compiled - deploy schema first
        logger.error("Query not found. Run 'helix deploy'")
    else:
        raise
```

### 4. Connection Management

```python
# Use context manager for auto-cleanup
class HelixDBContext:
    def __init__(self, config_path, **kwargs):
        self.adapter = HelixDBAdapter(config_path, **kwargs)
    
    async def __aenter__(self):
        return self.adapter
    
    async def __aexit__(self, *args):
        # Cleanup if needed
        pass

# Usage
async with HelixDBContext("./helixdb-cfg") as adapter:
    await adapter.add_node(entity)
```

### 5. Batch Operations

```python
# Batch insertions for better performance
async def batch_insert_nodes(adapter, nodes, batch_size=100):
    for i in range(0, len(nodes), batch_size):
        batch = nodes[i:i+batch_size]
        await adapter.add_nodes(batch)
        # Optional: add delay to avoid overwhelming instance
        await asyncio.sleep(0.1)
```

## Troubleshooting

### Common Issues

**Issue**: `ImportError: helix-py package is required`
```bash
pip install helix-py
```

**Issue**: `RuntimeError: Failed to initialize HelixDB client`
- Ensure HelixDB instance is running: `helix instances`
- Check port is correct (default: 6969)
- Verify config_path points to valid HelixDB config directory

**Issue**: `Query not found` error
- Ensure queries are defined in `.hx` files
- Run `helix check` to verify syntax
- Run `helix deploy` to compile and deploy queries

**Issue**: Slow vector search
- Check HNSW index parameters
- Consider reducing search space
- Monitor dataset size - performance degrades with very large datasets

**Issue**: Connection refused
- Start local instance: `helix deploy` in config directory
- Or verify remote endpoint is accessible

## Advanced Topics

### Custom Embeddings

```python
# Use HelixDB built-in embeddings (when available via SDK)
# Currently uses provided embedding_engine

# Example with OpenAI
from cognee.infrastructure.databases.vector.embeddings import EmbeddingEngine

embedding_engine = EmbeddingEngine(
    provider="openai",
    model="text-embedding-3-small"
)

adapter = HelixDBAdapter(
    config_path="./helixdb-cfg",
    embedding_engine=embedding_engine
)
```

### Schema Migration

```bash
# 1. Update schema in .hx files
# 2. Create migration script
helix check  # Verify new schema

# 3. Backup data (manual process currently)
# 4. Deploy new schema
helix deploy

# 5. Migrate data using custom script
# (Tool support for migrations is limited)
```

### Monitoring

```python
# Get graph metrics
metrics = await adapter.get_graph_metrics(include_optional=True)
print(f"Nodes: {metrics.get('node_count')}")
print(f"Edges: {metrics.get('edge_count')}")

# Monitor query performance
import time

start = time.time()
results = await adapter.search("collection", query_text="test", limit=10)
duration = time.time() - start
print(f"Search took {duration:.3f}s")
```

## Testing

```python
import pytest
from cognee.infrastructure.databases.hybrid.helixdb import HelixDBAdapter

@pytest.mark.asyncio
async def test_helixdb_adapter():
    adapter = HelixDBAdapter(
        config_path="./test-helixdb-cfg",
        auto_start=True
    )
    
    # Test operations
    await adapter.create_collection("test")
    # ... more tests
```

## Migration from Other Databases

### From Neo4j/Neptune

```python
# Neo4j Cypher -> HelixQL equivalents

# Cypher:
# MATCH (n:User {name: "Alice"}) RETURN n

# HelixQL:
# QUERY getUserByName(name: String) =>
#     user <- N<User::WHERE(_::{name}::EQ(name))>
#     RETURN user
```

### From Pinecone/Weaviate

```python
# Vector operations map directly
# pinecone.index.upsert() -> adapter.create_data_points()
# pinecone.index.query() -> adapter.search()
```

## Resources

- [HelixDB GitHub](https://github.com/HelixDB/helix-db)
- [HelixDB Documentation](https://docs.helix-db.com)
- [helix-py SDK](https://github.com/HelixDB/helix-py)
- [HelixQL Documentation](https://docs.helix-db.com/helix-ql/overview)
- [Cognee Documentation](https://docs.cognee.ai)

## Support

For issues specific to:
- **HelixDB**: [HelixDB Discord](https://discord.gg/2stgMPr5BD)
- **This Adapter**: Open an issue in the cognee repository
- **helix-py**: [helix-py GitHub Issues](https://github.com/HelixDB/helix-py/issues)

## Contributing

Contributions are welcome! Areas for improvement:

1. **Full Query Implementation**: Implement actual HelixQL queries for all operations
2. **Performance Optimization**: Optimize batch operations and caching
3. **Schema Management**: Better utilities for schema evolution
4. **Testing**: Comprehensive test suite
5. **Examples**: More real-world usage examples
6. **Documentation**: Additional guides and tutorials

## License

This adapter is part of the cognee project and follows its Apache 2.0 license.
