# Project Structure

## Main Package: `cognee/`

```
cognee/
├── api/                  # FastAPI application
│   └── v1/               # Versioned routers (21 total)
│       ├── add/          # Data ingestion
│       ├── cloud/        # Cloud sync
│       ├── cognify/      # Knowledge graph generation
│       ├── config/       # Configuration management
│       ├── datasets/     # Dataset management
│       ├── delete/       # Data deletion
│       ├── exceptions/   # API exceptions
│       ├── memify/       # Memory algorithms
│       ├── notebooks/    # Jupyter integration
│       ├── ontologies/   # Ontology management
│       ├── permissions/  # Access control
│       ├── prune/        # System reset
│       ├── responses/    # Response handling
│       ├── search/       # Query endpoints
│       ├── settings/     # Settings management
│       ├── sync/         # Sync operations
│       ├── thought_graph/# Thought graph endpoints
│       ├── ui/           # Web UI endpoints
│       ├── update/       # Data updates
│       ├── users/        # User management
│       └── visualize/    # Graph visualization
├── cli/                  # CLI entry points (cognee-cli)
│   └── commands/         # add, search, cognify, delete, config
├── infrastructure/       # Database adapters, LLM providers, loaders
│   ├── databases/
│   │   ├── graph/        # Kuzu, Neo4j, Neptune adapters
│   │   ├── vector/       # LanceDB, PGVector, Qdrant, etc.
│   │   ├── relational/   # SQLite, PostgreSQL
│   │   ├── hybrid/       # Hybrid database support
│   │   └── dataset_database_handler/  # Multi-user access
│   ├── llm/              # LLM gateway, extraction, prompts
│   └── loaders/          # Text, PDF, Audio, Image, CSV loaders
├── modules/              # Domain logic (23 modules)
│   ├── graph/            # Graph operations
│   ├── retrieval/        # Search and retrieval
│   ├── ontology/         # Ontology management
│   ├── cloud/            # Cloud sync
│   ├── thought_graph/    # Thought graphs
│   ├── metrics/          # Metrics collection
│   ├── notebooks/        # Notebook integration
│   ├── memify/           # Memory algorithms
│   ├── visualization/    # Graph visualization
│   └── ...
├── tasks/                # Reusable pipeline tasks (17 categories)
│   ├── chunks/           # Chunking tasks
│   ├── documents/        # Document processing
│   ├── graph/            # Graph tasks
│   ├── codingagents/     # Code analysis
│   ├── feedback/         # Feedback collection
│   ├── temporal_graph/   # Temporal awareness
│   └── ...
├── shared/               # Cross-cutting utilities
├── eval_framework/       # Evaluation utilities
├── memify_pipelines/     # Specialized memify pipelines
├── tests/                # Test suite
│   ├── unit/
│   ├── integration/
│   └── cli_tests/
└── __init__.py           # Public API exports
```

## Public API Exports (cognee/__init__.py)

- `add()`, `cognify()`, `memify()`, `search()`, `delete()`, `prune()`
- `update()`, `config()`, `datasets()`
- `visualize_graph()`, `start_visualization_server()`, `cognee_network_visualization()`
- `start_ui()`, `run_custom_pipeline()`, `pipelines`
- `SearchType` enum

## Companion Packages

- `cognee-mcp/` - Model Context Protocol server (SSE/HTTP/stdio)
- `cognee-frontend/` - Next.js 16 UI with React 19
- `cognee-starter-kit/` - Starter templates
- `cognee-aws-bedrock/` - AWS Bedrock integration

## Supporting Directories

- `alembic/` - Database migrations for relational backends
- `distributed/` - Distributed execution utilities (Modal, workers)
- `examples/` - Example scripts demonstrating APIs
- `new-examples/` - Reorganized examples by category
- `notebooks/` - Jupyter notebooks for demos
- `evals/` - Evaluation benchmarks and results

## Extension Points

- Add new tasks in `cognee/tasks/`
- Add new loaders in `cognee/infrastructure/loaders/`
- Add new retrievers in `cognee/modules/retrieval/`
- Add database adapters in `cognee/infrastructure/databases/`
- Add LLM providers in `cognee/infrastructure/llm/`

## Test Organization

- Unit tests: `cognee/tests/unit/`
- Integration tests: `cognee/tests/integration/`
- CLI tests: `cognee/tests/cli_tests/`
- Test files named `test_*.py`
- Use `pytest.mark.asyncio` for async tests
