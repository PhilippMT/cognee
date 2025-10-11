# HelixDB Adapter - Quick Start Guide

**⚡ Get started with HelixDB hybrid adapter in 5 minutes**

## 🎯 What You'll Learn

- How to install and setup HelixDB
- How to use the adapter in your code
- What you need to do to make it fully functional

## ⚠️ Important First

**This adapter is a stub/skeleton implementation.** It provides the interface structure but requires you to:
1. Define your schema in `.hx` files
2. Write HelixQL queries for operations
3. Compile and deploy queries

See [README.md](./README.md) for complete guide or [LIMITATIONS.md](./LIMITATIONS.md) for all constraints.

## 📦 Step 1: Install Dependencies

### Install HelixDB CLI
```bash
curl -fsSL "https://install.helix-db.com" | bash
```

### Install Python SDK
```bash
pip install helix-py
```

### Verify Installation
```bash
helix --version
python -c "import helix; print('helix-py installed')"
```

## 🏗️ Step 2: Setup HelixDB Project

### Create Project
```bash
# Create directory for your config
mkdir my-helixdb-project
cd my-helixdb-project

# Initialize HelixDB
helix install
helix setup
```

This creates a directory structure:
```
my-helixdb-project/
├── schema.hx      # Define your data schema
├── queries.hx     # Define your queries
└── config/        # HelixDB configuration
```

## 📝 Step 3: Define Your Schema

Edit `schema.hx`:

```helix
# Define node types
NODE Document {
    id: String,
    content: String,
    metadata: String,
    embedding: Vec<F64>  # Vector for similarity search
}

NODE Entity {
    id: String,
    name: String,
    description: String,
    type: String
}

# Define relationships
EDGE CONTAINS {
    Document -> Entity
}

EDGE RELATES_TO {
    Entity -> Entity,
    confidence: F64
}
```

**Important**: Vector dimension must match your embedding model (e.g., 1536 for OpenAI).

## 🔍 Step 4: Write Basic Queries

Edit `queries.hx`:

```helix
# Add a document node
QUERY addDocument(id: String, content: String, vec: Vec<F64>) =>
    doc <- AddN<Document({
        id: id,
        content: content,
        embedding: vec
    })>
    RETURN doc

# Search documents by vector similarity
QUERY searchDocuments(query_vec: Vec<F64>, limit: I64) =>
    docs <- VecSearch<Document>(query_vec, topk: limit)
    RETURN docs

# Add an entity node
QUERY addEntity(id: String, name: String, desc: String) =>
    entity <- AddN<Entity({
        id: id,
        name: name,
        description: desc
    })>
    RETURN entity

# Get entity by ID
QUERY getEntity(entity_id: String) =>
    entity <- N<Entity::WHERE(_::{id}::EQ(entity_id))>
    RETURN entity

# Add relationship between nodes
QUERY addRelationship(source_id: String, target_id: String) =>
    source <- N<Entity::WHERE(_::{id}::EQ(source_id))>
    target <- N<Entity::WHERE(_::{id}::EQ(target_id))>
    edge <- AddE<RELATES_TO(source, target)>
    RETURN edge
```

## ✅ Step 5: Validate and Deploy

### Check syntax
```bash
helix check
```

### Deploy to local instance
```bash
helix deploy
```

This compiles your queries and starts a local HelixDB instance on port 6969.

## 🐍 Step 6: Use the Adapter

### Basic Usage

```python
from cognee.infrastructure.databases.hybrid.helixdb import HelixDBAdapter
from cognee.infrastructure.databases.vector.embeddings import get_embedding_engine

# Initialize adapter
embedding_engine = get_embedding_engine()
adapter = HelixDBAdapter(
    config_path="./my-helixdb-project",
    port=6969,
    local=True,
    embedding_engine=embedding_engine
)

# Now the adapter is ready to use!
```

### Example: Add a Document

```python
import asyncio
from cognee.infrastructure.engine import DataPoint

class MyDocument(DataPoint):
    content: str
    metadata: dict = {"index_fields": ["content"]}

async def add_document():
    doc = MyDocument(
        id="doc1",
        content="HelixDB is a fast graph-vector database"
    )
    
    # Get embedding
    embedding = await adapter.embed_data([doc.content])
    
    # Call your deployed query
    result = await adapter.query(
        "addDocument",
        {
            "id": str(doc.id),
            "content": doc.content,
            "vec": embedding[0]
        }
    )
    print(f"Added document: {result}")

asyncio.run(add_document())
```

### Example: Search Documents

```python
async def search_documents():
    # Get query vector
    query = "fast database"
    query_vec = await adapter.embed_data([query])
    
    # Call your search query
    results = await adapter.query(
        "searchDocuments",
        {
            "query_vec": query_vec[0],
            "limit": 5
        }
    )
    print(f"Found {len(results)} results")
    for result in results:
        print(f"- {result}")

asyncio.run(search_documents())
```

## 🔧 Step 7: Update Adapter Methods (Optional)

To make the adapter methods work automatically, update `HelixDBAdapter.py`:

```python
# In HelixDBAdapter.py

async def create_data_points(self, collection_name: str, data_points: List[DataPoint]):
    """Insert data points (now with real implementation)"""
    self._validate_embedding_engine()
    
    texts = [DataPoint.get_embeddable_data(dp) for dp in data_points]
    vectors = await self.embedding_engine.embed_text(texts)
    
    results = []
    for index, data_point in enumerate(data_points):
        result = await self.query(
            "addDocument",  # Your query name
            {
                "id": str(data_point.id),
                "content": getattr(data_point, "content", ""),
                "vec": vectors[index]
            }
        )
        results.append(result)
    
    return results
```

## 🧪 Step 8: Test Your Setup

```python
import asyncio
from cognee.infrastructure.databases.hybrid.helixdb import HelixDBAdapter
from cognee.infrastructure.databases.vector.embeddings import get_embedding_engine
from cognee.infrastructure.engine import DataPoint

class TestDocument(DataPoint):
    content: str
    metadata: dict = {"index_fields": ["content"]}

async def test_helixdb():
    # Initialize
    embedding_engine = get_embedding_engine()
    adapter = HelixDBAdapter(
        config_path="./my-helixdb-project",
        embedding_engine=embedding_engine
    )
    
    # Create test document
    doc = TestDocument(
        id="test1",
        content="This is a test document"
    )
    
    # Get embedding
    embedding = await adapter.embed_data([doc.content])
    
    # Add document using your query
    print("Adding document...")
    result = await adapter.query(
        "addDocument",
        {
            "id": str(doc.id),
            "content": doc.content,
            "vec": embedding[0]
        }
    )
    print(f"✓ Added: {result}")
    
    # Search
    print("\nSearching...")
    search_results = await adapter.query(
        "searchDocuments",
        {
            "query_vec": embedding[0],
            "limit": 1
        }
    )
    print(f"✓ Found: {len(search_results)} results")
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    asyncio.run(test_helixdb())
```

Run the test:
```bash
python test_helixdb.py
```

## 📚 Next Steps

### Learn More
- [README.md](./README.md) - Complete usage guide
- [ANALYSIS.md](./ANALYSIS.md) - Technical deep-dive
- [LIMITATIONS.md](./LIMITATIONS.md) - All limitations
- [example_usage.py](./example_usage.py) - More examples

### Add More Queries
1. Define more queries in `queries.hx`
2. Run `helix check` to validate
3. Run `helix deploy` to update
4. Use new queries in your code

### Common Queries to Add

```helix
# Update a document
QUERY updateDocument(id: String, content: String) =>
    doc <- N<Document::WHERE(_::{id}::EQ(id))>
    updated <- Update<doc({content: content})>
    RETURN updated

# Delete a document
QUERY deleteDocument(id: String) =>
    doc <- N<Document::WHERE(_::{id}::EQ(id))>
    Delete<doc>
    RETURN "deleted"

# Get all neighbors of an entity
QUERY getNeighbors(entity_id: String) =>
    entity <- N<Entity::WHERE(_::{id}::EQ(entity_id))>
    neighbors <- Out<entity>
    RETURN neighbors

# Get document with entities
QUERY getDocumentWithEntities(doc_id: String) =>
    doc <- N<Document::WHERE(_::{id}::EQ(doc_id))>
    entities <- Out<doc>
    RETURN {doc: doc, entities: entities}
```

## 🐛 Troubleshooting

### Error: "helix-py not installed"
```bash
pip install helix-py
```

### Error: "Failed to initialize HelixDB client"
```bash
# Check if instance is running
helix instances

# If not, deploy again
cd my-helixdb-project
helix deploy
```

### Error: "Query not found"
```bash
# Recompile queries
cd my-helixdb-project
helix check
helix deploy
```

### Port already in use
```bash
# Stop existing instance
helix stop --all

# Or use different port
adapter = HelixDBAdapter(
    config_path="./my-helixdb-project",
    port=7000,  # Different port
    embedding_engine=embedding_engine
)
```

## ⚡ Quick Reference

### Essential Commands
```bash
helix install          # Install HelixDB
helix setup            # Create new project
helix check            # Validate syntax
helix deploy           # Compile and deploy
helix instances        # List running instances
helix stop --all       # Stop all instances
```

### Essential Code
```python
# Initialize
from cognee.infrastructure.databases.hybrid.helixdb import HelixDBAdapter
adapter = HelixDBAdapter(config_path="./path", embedding_engine=engine)

# Execute query
result = await adapter.query("queryName", {"param": "value"})

# Get embeddings
vectors = await adapter.embed_data(["text1", "text2"])
```

## 🎓 Learning Path

1. ✅ Complete this Quick Start
2. ✅ Read [README.md](./README.md) for detailed usage
3. ✅ Review [example_usage.py](./example_usage.py) for patterns
4. ✅ Study [LIMITATIONS.md](./LIMITATIONS.md) to understand constraints
5. ✅ Read [ANALYSIS.md](./ANALYSIS.md) for deep technical understanding
6. ✅ Explore [HelixDB Docs](https://docs.helix-db.com) for HelixQL details

## 💡 Tips

- **Start Simple**: Begin with basic queries, add complexity gradually
- **Pin Versions**: `pip install helix-py==0.2.30` for stability
- **Version Control**: Keep your `.hx` files in git
- **Test Locally**: Always test queries locally before deploying
- **Monitor Performance**: Log query times to optimize
- **Backup Data**: HelixDB data is in LMDB files, backup regularly

## 🤝 Getting Help

- **HelixDB Discord**: [discord.gg/2stgMPr5BD](https://discord.gg/2stgMPr5BD)
- **GitHub Issues**: [github.com/HelixDB/helix-db/issues](https://github.com/HelixDB/helix-db/issues)
- **Documentation**: [docs.helix-db.com](https://docs.helix-db.com)

## ✅ Checklist

- [ ] Installed HelixDB CLI
- [ ] Installed helix-py
- [ ] Created HelixDB project
- [ ] Defined schema in `.hx` file
- [ ] Wrote basic queries
- [ ] Validated with `helix check`
- [ ] Deployed with `helix deploy`
- [ ] Tested adapter connection
- [ ] Successfully executed first query
- [ ] Read LIMITATIONS.md

Once you've checked all boxes, you're ready to build with HelixDB! 🚀

---

**Time to Complete**: ~15-30 minutes  
**Difficulty**: Medium  
**Prerequisites**: Python 3.10+, Basic async/await knowledge
