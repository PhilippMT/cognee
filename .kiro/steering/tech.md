# Tech Stack & Build System

## Language & Runtime

- Python 3.10 - 3.13
- Package manager: `uv` (recommended) or Poetry
- Build backend: Hatchling

## Core Dependencies

- FastAPI 0.116+ - REST API framework
- Pydantic 2.10+ / pydantic-settings - Data validation and settings
- SQLAlchemy 2.0+ / Alembic - Relational DB ORM and migrations
- LiteLLM 1.76+ / Instructor 1.9+ - LLM abstraction and structured outputs
- LanceDB 0.24+ (default) - Vector database
- Kuzu 0.11+ (default) - Graph database
- fastembed - Embedding generation
- Uvicorn / Gunicorn - ASGI servers

## Structured Output Frameworks

- Instructor (default) - LiteLLM-based structured outputs
- BAML (optional) - Alternative structured output framework

## Default Storage (file-based, no setup required)

- Relational: SQLite
- Vector: LanceDB
- Graph: Kuzu

## Optional Integrations

- Graph: Neo4j, Neptune Analytics, Kuzu Remote
- Vector: PGVector, ChromaDB, Qdrant, Weaviate, Milvus
- LLM: OpenAI, Azure, Anthropic, Ollama, Mistral, Groq, custom endpoints
- Storage: S3 (with s3fs + boto3), PostgreSQL
- Monitoring: Sentry, Langfuse, PostHog
- Integrations: LangChain, LlamaIndex, HuggingFace, Graphiti, dlt

## Common Commands

```bash
# Install dependencies
uv sync --dev --all-extras --reinstall

# Run CLI
uv run cognee-cli add "text"
uv run cognee-cli cognify
uv run cognee-cli search "query"
uv run cognee-cli -ui  # Launch UI + API + MCP
uv run cognee-cli --debug add "text"  # Debug mode

# Start API server
uv run python -m cognee.api.client

# Run tests
uv run pytest cognee/tests/unit/ -v
uv run pytest cognee/tests/integration/ -v

# Lint and format
uv run ruff check .
uv run ruff format .

# Type checking (optional)
uv run mypy cognee/
```

## Frontend (cognee-frontend/)

Next.js 16 with React 19, TailwindCSS, D3 Force Graph visualization.

```bash
npm install
npm run dev
npm run lint
npm run build && npm start
```

## MCP Server (cognee-mcp/)

Supports stdio (default), SSE, and HTTP transports. Can run in direct mode or API mode.

```bash
uv sync --dev --all-extras --reinstall
uv run python src/server.py  # stdio default
uv run python src/server.py --transport sse
uv run python src/server.py --transport http --host 127.0.0.1 --port 8000 --path /mcp
# API mode
uv run python src/server.py --transport sse --api-url http://localhost:8000 --api-token TOKEN
```

## Key Environment Variables

```bash
# LLM Configuration
LLM_API_KEY="your_api_key"
LLM_MODEL="openai/gpt-5-mini"
LLM_PROVIDER="openai"
STRUCTURED_OUTPUT_FRAMEWORK="instructor"  # or "baml"

# Embedding Configuration
EMBEDDING_PROVIDER="openai"
EMBEDDING_MODEL="openai/text-embedding-3-large"

# Storage Backend
STORAGE_BACKEND="local"  # or "s3"
STORAGE_BUCKET_NAME="your-bucket"  # for S3

# Database Providers
DB_PROVIDER="sqlite"  # or "postgres"
GRAPH_DATABASE_PROVIDER="kuzu"  # or "neo4j", "neptune"
VECTOR_DB_PROVIDER="lancedb"  # or "pgvector", "qdrant", etc.

# Multi-user Support
ENABLE_BACKEND_ACCESS_CONTROL="false"
```

## Code Style

- Line length: 100 (configured in pyproject.toml)
- Formatter/Linter: ruff
- Naming: `snake_case` for modules/functions, `PascalCase` for classes
- Type annotations encouraged for public APIs
