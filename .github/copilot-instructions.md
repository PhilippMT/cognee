# Cognee AI Copilot Instructions

## Identity

You are an AI assistant helping developers work on **cognee** - an open-source memory layer for AI agents that provides semantic understanding through knowledge graphs and vector databases. You assist with implementing features, fixing bugs, writing tests, and maintaining code quality while following the project's established patterns and conventions.

## Project Overview

**cognee** is a Python library that builds dynamic memory for AI agents using scalable, modular ECL (Extract, Cognify, Load) pipelines. It transforms unstructured data into interconnected knowledge graphs and vector embeddings, replacing traditional RAG systems with a sophisticated memory layer.

### Key Technologies
- **Python 3.10-3.13**: Core implementation language
- **AsyncIO**: Asynchronous operations throughout
- **Pydantic**: Data validation and settings management
- **SQLAlchemy**: Database ORM and migrations with Alembic
- **FastAPI**: Web server and REST API
- **LiteLLM**: Multi-provider LLM integration (OpenAI, Anthropic, Gemini, etc.)
- **Vector Databases**: LanceDB (default), Qdrant, Weaviate, PGVector
- **Graph Databases**: Kuzu (default), Neo4j, Memgraph, Neptune
- **Testing**: pytest with pytest-asyncio and pytest-cov

### Architecture Summary
- **cognee/api/**: REST API endpoints (v1)
- **cognee/infrastructure/**: Core infrastructure (databases, LLM, files, loaders)
- **cognee/modules/**: Feature modules (cognify, memify, search, pipelines)
- **cognee/tasks/**: Individual task implementations for pipelines
- **cognee/shared/**: Shared utilities and logging
- **cognee/tests/**: Test suite (unit, integration, CLI tests)
- **examples/**: Usage examples and demos
- **cognee-mcp/**: Model Context Protocol server implementation

## Related Documentation

Always check these resources when working on the project:

1. **[README.md](../README.md)** - Project overview, installation, and basic usage
2. **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Contribution guidelines and workflow
3. **[Documentation](https://docs.cognee.ai)** - Comprehensive online documentation
4. **[CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md)** - Community standards
5. **[.env.template](../.env.template)** - Environment configuration reference

## Development Environment Setup

### Prerequisites
```bash
# Python 3.10-3.13 required
python --version

# Install using uv (recommended)
uv pip install -e ".[dev,postgres,neo4j,docs]"

# Or using pip
pip install -e ".[dev,postgres,neo4j,docs]"

# Or using poetry
poetry install --extras "dev postgres neo4j docs"
```

### Environment Configuration
Copy `.env.template` to `.env` and configure:
```bash
# Required
LLM_API_KEY=your_openai_api_key

# Optional - Use defaults or configure as needed
GRAPH_DATABASE_PROVIDER=kuzu  # kuzu, neo4j, memgraph, neptune
VECTOR_DB_PROVIDER=lancedb    # lancedb, qdrant, weaviate, pgvector
```

### Code Quality Tools
```bash
# Format code with ruff
ruff format .

# Run linter
ruff check .

# Type checking with mypy
mypy cognee/

# Pre-commit hooks (recommended)
pre-commit install
pre-commit run --all-files
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cognee

# Run specific test file
pytest cognee/tests/test_library.py

# Run specific test
pytest cognee/tests/test_library.py::test_function_name

# Run async tests
pytest -v -s cognee/tests/test_library.py
```

## Development Workflow

### Before Making Changes
1. **Create a branch from `dev`**: `git checkout -b feature/your-feature-name dev`
2. **Review similar implementations**: Check existing code for patterns
3. **Read documentation**: Check docs.cognee.ai for relevant context
4. **Set up environment**: Ensure all dependencies are installed
5. **Run tests**: Verify starting state with `pytest`

### While Developing
1. **Follow async patterns**: All I/O operations should be async
2. **Use type hints**: Add proper type annotations to all functions
3. **Add docstrings**: Document public APIs with clear descriptions
4. **Handle errors gracefully**: Use proper exception handling with informative messages
5. **Log appropriately**: Use the shared logging system
6. **Write tests first**: TDD approach when adding features
7. **Keep changes minimal**: Make surgical, focused changes

### Code Standards

#### Async Patterns
```python
# ✅ CORRECT - Async functions with proper await
async def process_data(data: str) -> dict:
    """Process data asynchronously."""
    result = await cognee.add(data)
    await cognee.cognify()
    return await cognee.search("query")

# ❌ WRONG - Missing async/await
def process_data(data: str) -> dict:
    result = cognee.add(data)  # Will fail
    return result
```

#### Type Hints
```python
# ✅ CORRECT - Proper type annotations
from typing import Optional, List, Dict, Any

async def search_memory(
    query: str,
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """Search the knowledge graph with optional filters."""
    pass

# ❌ WRONG - No type hints
async def search_memory(query, filters=None, limit=10):
    pass
```

#### Error Handling
```python
# ✅ CORRECT - Descriptive error handling
from cognee.shared.logging_utils import get_logger

logger = get_logger(__name__)

async def process_file(file_path: str) -> None:
    """Process a file and add to cognee."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        await cognee.add(file_path)
        logger.info(f"Successfully processed file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to process file {file_path}: {e}")
        raise

# ❌ WRONG - Bare except and no logging
async def process_file(file_path):
    try:
        await cognee.add(file_path)
    except:
        pass
```

#### Configuration Management
```python
# ✅ CORRECT - Use config system
import cognee

cognee.config.data_root_directory("/path/to/data")
cognee.config.llm_api_key("your-key")

# ❌ WRONG - Direct environment variable access
import os
api_key = os.getenv("LLM_API_KEY")
```

### Testing Requirements

#### Test Structure
```python
import pytest
from pathlib import Path
import cognee

@pytest.mark.asyncio
async def test_add_and_cognify():
    """Test adding data and running cognify pipeline."""
    # Setup
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    
    # Test data
    text = "Test content for knowledge graph."
    
    # Execute
    await cognee.add([text], "test_dataset")
    await cognee.cognify(["test_dataset"])
    
    # Verify
    results = await cognee.search("knowledge graph")
    assert len(results) > 0
    assert any("knowledge" in str(r).lower() for r in results)

@pytest.mark.asyncio
async def test_error_handling():
    """Test proper error handling for invalid input."""
    with pytest.raises(ValueError):
        await cognee.add(None)
```

#### Test Best Practices
- Use `@pytest.mark.asyncio` for async tests
- Always clean up test data with `prune_data()` and `prune_system()`
- Test both success and failure paths
- Use descriptive test names: `test_<feature>_<scenario>_<expected_result>`
- Mock external services (LLM, databases) when appropriate
- Keep tests independent and idempotent

### Common Patterns

#### Pipeline Tasks
```python
from cognee.modules.pipelines.tasks.task import Task
from typing import List, Any

# Define task input/output types
async def extract_entities(
    chunks: List[str],
) -> List[Dict[str, Any]]:
    """Extract entities from text chunks.
    
    Args:
        chunks: List of text chunks to process
        
    Returns:
        List of extracted entities with metadata
    """
    entities = []
    for chunk in chunks:
        # Process chunk
        entity = await process_chunk(chunk)
        entities.append(entity)
    
    return entities

# Register as pipeline task
extract_entities_task = Task(extract_entities)
```

#### Database Operations
```python
# Vector database
from cognee.infrastructure.databases.vector import get_vector_engine

vector_engine = get_vector_engine()
results = await vector_engine.search("Entity", query="AI", limit=10)

# Graph database
from cognee.infrastructure.databases.graph import get_graph_engine

graph_engine = await get_graph_engine()
nodes, edges = await graph_engine.get_nodeset_subgraph(
    node_type=NodeType,
    node_name=["node_set_name"]
)
```

#### LLM Integration
```python
from cognee.infrastructure.llm import LLMGateway
from cognee.infrastructure.llm.prompts import render_prompt

# Use LLM with structured output
llm_gateway = LLMGateway()
response = await llm_gateway.generate_structured_output(
    system_prompt=render_prompt("system_prompt.txt", context=context),
    user_prompt=render_prompt("user_prompt.txt", data=data),
    response_model=YourPydanticModel,
)
```

## Code Style Guidelines

### Formatting
- **Line length**: 100 characters (enforced by ruff)
- **Indentation**: 4 spaces
- **Imports**: Organized with isort (automated by ruff)
- **String quotes**: Double quotes preferred
- **Trailing commas**: Use for multi-line structures

### Naming Conventions
- **Functions/variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private members**: `_leading_underscore`
- **Modules**: `lowercase` or `snake_case`

### Documentation
```python
async def add_data(
    data: Union[str, List[str], Path],
    dataset_name: str = "default",
    node_set: Optional[List[str]] = None,
) -> None:
    """Add data to cognee for processing.
    
    This function ingests various types of data (text, files, URLs) and prepares
    them for the cognify pipeline. Data can be organized into datasets and node sets
    for better organization and retrieval.
    
    Args:
        data: Text string, file path(s), or URL(s) to add
        dataset_name: Name of the dataset to add data to. Defaults to "default"
        node_set: Optional list of node set names to organize the data
        
    Returns:
        None
        
    Raises:
        ValueError: If data is None or empty
        FileNotFoundError: If file path does not exist
        
    Example:
        >>> await cognee.add("Important information about AI")
        >>> await cognee.add("/path/to/file.pdf", dataset_name="docs")
        >>> await cognee.add(["file1.txt", "file2.txt"], node_set=["research"])
    """
    pass
```

## Common Development Tasks

### Adding a New API Endpoint
1. Create endpoint in `cognee/api/v1/<module>/<endpoint>.py`
2. Define request/response models with Pydantic
3. Implement handler with proper error handling
4. Add tests in `cognee/tests/integration/`
5. Update API documentation

### Adding a New Pipeline Task
1. Create task in `cognee/tasks/<category>/<task_name>.py`
2. Implement async function with clear input/output types
3. Add task to appropriate pipeline configuration
4. Write unit tests in `cognee/tests/tasks/`
5. Document task behavior and parameters

### Adding Support for New LLM Provider
1. Check if LiteLLM already supports it
2. If not, extend `cognee/infrastructure/llm/llm_interface.py`
3. Add configuration in `cognee/base_config.py`
4. Update `.env.template` with new provider settings
5. Add integration tests
6. Update documentation

### Adding Support for New Database
1. Implement adapter in `cognee/infrastructure/databases/<type>/<provider>.py`
2. Follow existing adapter patterns (e.g., `kuzu_adapter.py`)
3. Add configuration in `base_config.py`
4. Update `.env.template`
5. Add integration tests
6. Update documentation

## Security Guidelines

- **Never commit secrets**: Use environment variables via `.env`
- **Validate all inputs**: Especially user-provided data
- **Sanitize file paths**: Prevent directory traversal attacks
- **Use parameterized queries**: Prevent SQL injection
- **Log safely**: Don't log sensitive data (API keys, user data)
- **Handle permissions**: Check user permissions before operations
- **Secure defaults**: Use secure default configurations

## Performance Considerations

- **Batch operations**: Process data in batches when possible
- **Use async/await**: Maximize concurrent operations
- **Stream large files**: Don't load entire files into memory
- **Cache appropriately**: Cache LLM responses and embeddings
- **Index databases**: Ensure proper indexes on frequently queried fields
- **Profile before optimizing**: Use profiling tools to find bottlenecks

## Debugging Tips

### Enable Debug Logging
```python
# In code
from cognee.shared.logging_utils import setup_logging, DEBUG
logger = setup_logging(log_level=DEBUG)

# Or set environment variable
export LOG_LEVEL=DEBUG
```

### Common Issues

**Issue**: `ModuleNotFoundError`
- **Solution**: Ensure dependencies are installed: `uv pip install -e ".[dev]"`

**Issue**: `RuntimeError: Event loop is closed`
- **Solution**: Use proper async context, avoid mixing sync/async code

**Issue**: Database connection errors
- **Solution**: Check `.env` configuration, ensure database is running

**Issue**: LLM API errors
- **Solution**: Verify `LLM_API_KEY` is set, check API quota/limits

## Contributing

### Pull Request Guidelines
1. **Branch from `dev`**: All PRs should target the `dev` branch
2. **Clear description**: Explain what and why, not just how
3. **Tests included**: All new features need tests
4. **Tests passing**: Ensure all tests pass before submitting
5. **Code formatted**: Run `ruff format .` before committing
6. **Signed commits**: Use DCO sign-off: `git commit -s`
7. **Small PRs**: Keep changes focused and reviewable

### PR Title Format
```
<type>: <short description>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- test: Adding or updating tests
- refactor: Code refactoring
- perf: Performance improvements
- chore: Maintenance tasks
```

### PR Description Template
```markdown
## Summary
Brief description of the changes

## Changes
- Added X feature to Y module
- Fixed Z bug in A component
- Refactored B for better performance

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Documentation updated

## Related Issues
Closes #123
```

## Project-Specific Notes

### Branch Strategy
- **`main`**: Stable production releases
- **`dev`**: Active development branch (PR target)
- **Feature branches**: `feature/description` or `fix/description`

### Cognee Core Concepts
1. **Add**: Ingest data into the system
2. **Cognify**: Process data into knowledge graph
3. **Memify**: Add memory algorithms to enhance the graph
4. **Search**: Query the knowledge graph with semantic understanding
5. **Prune**: Clean up data and system state

### Important Abstractions
- **DataPoint**: Base class for graph nodes
- **NodeSet**: Collections of related nodes
- **Task**: Pipeline task unit
- **Pipeline**: Sequence of tasks for data processing
- **Engine**: Database/service abstraction layer

## Support and Resources

- **Documentation**: https://docs.cognee.ai
- **Discord**: https://discord.gg/NQPKmU5CCg
- **Issues**: https://github.com/topoteretes/cognee/issues
- **Discussions**: https://github.com/topoteretes/cognee/discussions
- **Email**: vasilije@cognee.ai (for sensitive matters)

## License

This project is licensed under Apache 2.0. Ensure all contributions comply with this license.

---

**Remember**: The goal is to build reliable, maintainable, and well-tested code that helps developers create intelligent AI agents with sophisticated memory systems. Focus on clarity, correctness, and consistency in all contributions.
