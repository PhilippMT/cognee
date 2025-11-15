# GitHub Copilot Adapter - Detailed Usage Guide

This guide provides comprehensive information on using the GitHub Copilot adapter with Cognee.

## Table of Contents

1. [Installation](#installation)
2. [Authentication](#authentication)
3. [Basic Configuration](#basic-configuration)
4. [Model Selection](#model-selection)
5. [Complete Workflow Examples](#complete-workflow-examples)
6. [Advanced Usage](#advanced-usage)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites

- Python 3.10 or higher
- GitHub Copilot Pro+ subscription (or higher)
- GitHub Personal Access Token with Copilot access

### Install Package

```bash
# Install from local directory
pip install -e cognee-github-copilot/

# Or if installing as part of cognee
pip install cognee
pip install -e cognee-github-copilot/
```

## Authentication

### Using Environment Variable (Recommended)

```bash
export GITHUB_TOKEN=your_github_token
```

Then in your code:

```python
from cognee_github_copilot import register_github_copilot_adapters

register_github_copilot_adapters()
```

### Using API Key in Code

```python
from cognee_github_copilot import register_github_copilot_adapters

register_github_copilot_adapters(
    api_key="your-github-token"
)
```

### Getting a GitHub Token

1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with Copilot permissions
3. Save the token securely

## Basic Configuration

### Minimal Setup

```python
import cognee
from cognee_github_copilot import register_github_copilot_adapters

# Register adapter
register_github_copilot_adapters()

# Configure LLM
cognee.config.llm_provider = "github_copilot"
cognee.config.llm_model = "gpt-4o"

# Configure embeddings (required - GitHub Copilot doesn't provide embeddings)
cognee.config.embedding_provider = "openai"
cognee.config.embedding_model = "text-embedding-3-small"
```

### Full Configuration

```python
import cognee
import os
from cognee_github_copilot import register_github_copilot_adapters

# Set environment variables
os.environ["GITHUB_TOKEN"] = "your-token"
os.environ["LLM_API_KEY"] = "your-openai-key"  # For embeddings

# Register adapter
register_github_copilot_adapters()

# LLM Configuration
cognee.config.llm_provider = "github_copilot"
cognee.config.llm_model = "claude-sonnet-4"
cognee.config.llm_temperature = 0.0
cognee.config.llm_max_completion_tokens = 16384

# Embedding Configuration
cognee.config.embedding_provider = "openai"
cognee.config.embedding_model = "text-embedding-3-small"
cognee.config.embedding_dimensions = 1536

# Rate Limiting (optional)
cognee.config.llm_rate_limit_enabled = True
cognee.config.llm_rate_limit_requests = 60
cognee.config.llm_rate_limit_interval = 60
```

## Model Selection

### By Use Case

#### Speed-Critical Applications

```python
# Fastest models
cognee.config.llm_model = "gemini-2.0-flash"  # 0.25x multiplier
# cognee.config.llm_model = "grok-code-fast-1"  # 0.25x multiplier
# cognee.config.llm_model = "gpt-4o"  # 0x multiplier
```

#### Cost-Sensitive Projects

```python
# Zero-cost models (included in base plan)
cognee.config.llm_model = "gpt-4.1"  # 0x multiplier
# cognee.config.llm_model = "gpt-4o"  # 0x multiplier
# cognee.config.llm_model = "gpt-5-mini"  # 0x multiplier
```

#### Complex Reasoning Tasks

```python
# Best reasoning models
cognee.config.llm_model = "o3"  # Extended reasoning
# cognee.config.llm_model = "claude-sonnet-3.7-thinking"  # Visible reasoning
# cognee.config.llm_model = "claude-opus-4.1"  # Advanced reasoning
```

#### Large Codebase Analysis

```python
# Large context models
cognee.config.llm_model = "gemini-2.5-pro"  # 1M+ tokens
# cognee.config.llm_model = "gemini-2.0-flash"  # 1M tokens
# cognee.config.llm_model = "claude-opus-4"  # 200K tokens
```

### Model Switching

```python
# Dynamically switch models
models = ["gpt-4o", "claude-sonnet-4", "gemini-2.0-flash"]

for model in models:
    cognee.config.llm_model = model
    # Use cognee...
```

## Complete Workflow Examples

### Example 1: Document Processing

```python
import asyncio
import cognee
from cognee_github_copilot import register_github_copilot_adapters

async def process_documents():
    # Setup
    register_github_copilot_adapters()
    cognee.config.llm_provider = "github_copilot"
    cognee.config.llm_model = "claude-sonnet-4"
    cognee.config.embedding_provider = "openai"
    cognee.config.embedding_model = "text-embedding-3-small"
    
    # Clean previous data
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    
    # Add documents
    documents = [
        "Document 1 content...",
        "Document 2 content...",
        "Document 3 content...",
    ]
    
    await cognee.add(documents, "my_documents")
    
    # Build knowledge graph
    await cognee.cognify(["my_documents"])
    
    # Search
    results = await cognee.search("What are the main topics?")
    return results

# Run
results = asyncio.run(process_documents())
```

### Example 2: Multi-Model Comparison

```python
import asyncio
import cognee
from cognee_github_copilot import register_github_copilot_adapters

async def compare_models():
    register_github_copilot_adapters()
    cognee.config.embedding_provider = "openai"
    cognee.config.embedding_model = "text-embedding-3-small"
    
    data = "AI is transforming software development."
    query = "How is AI changing development?"
    
    models = {
        "gpt-4o": "OpenAI - Fast",
        "claude-sonnet-4": "Anthropic - Balanced",
        "gemini-2.0-flash": "Google - Efficient",
    }
    
    results = {}
    
    for model, description in models.items():
        print(f"\nTesting {model} ({description})...")
        
        cognee.config.llm_provider = "github_copilot"
        cognee.config.llm_model = model
        
        await cognee.prune.prune_data()
        await cognee.add([data], f"test_{model}")
        await cognee.cognify([f"test_{model}"])
        
        search_results = await cognee.search(query)
        results[model] = search_results
        
        print(f"  Found {len(search_results)} results")
    
    return results

# Run
results = asyncio.run(compare_models())
```

### Example 3: File Processing

```python
import asyncio
import cognee
from pathlib import Path
from cognee_github_copilot import register_github_copilot_adapters

async def process_files():
    register_github_copilot_adapters()
    cognee.config.llm_provider = "github_copilot"
    cognee.config.llm_model = "gpt-4o"
    cognee.config.embedding_provider = "openai"
    cognee.config.embedding_model = "text-embedding-3-small"
    
    # Process files
    files = [
        Path("file1.txt"),
        Path("file2.pdf"),
        Path("file3.md"),
    ]
    
    await cognee.add(files, "documents")
    await cognee.cognify(["documents"])
    
    # Search
    results = await cognee.search("summary of documents")
    return results

# Run
results = asyncio.run(process_files())
```

## Advanced Usage

### Custom Headers

The adapter automatically includes GitHub Copilot headers, but you can customize if needed:

```python
# Headers are automatically set:
# - editor-version: vscode/1.85.1
# - Copilot-Integration-Id: vscode-chat
```

### Fallback Models

Configure fallback models for error handling:

```python
from cognee.infrastructure.llm.config import get_llm_config

llm_config = get_llm_config()
llm_config.fallback_model = "gpt-5-mini"
llm_config.fallback_api_key = "backup-token"
```

### Rate Limiting

Control API rate limits:

```python
cognee.config.llm_rate_limit_enabled = True
cognee.config.llm_rate_limit_requests = 100
cognee.config.llm_rate_limit_interval = 60  # seconds

cognee.config.embedding_rate_limit_enabled = True
cognee.config.embedding_rate_limit_requests = 100
cognee.config.embedding_rate_limit_interval = 60
```

## Best Practices

### 1. Model Selection

- Use **gpt-4o** or **gpt-5-mini** for general-purpose tasks (0x multiplier)
- Use **claude-sonnet-4** for balanced performance
- Use **gemini-2.0-flash** for speed-critical applications
- Use **o3** or **claude-opus-4.1** for complex reasoning

### 2. Token Management

```python
# Set appropriate token limits
cognee.config.llm_max_completion_tokens = 4096  # For shorter responses
# cognee.config.llm_max_completion_tokens = 16384  # For longer responses
```

### 3. Error Handling

```python
try:
    await cognee.cognify()
except Exception as e:
    print(f"Error: {e}")
    # Handle error or retry with different model
```

### 4. Embedding Configuration

Always configure embeddings separately:

```python
# GitHub Copilot for LLM
cognee.config.llm_provider = "github_copilot"
cognee.config.llm_model = "gpt-4o"

# Separate provider for embeddings
cognee.config.embedding_provider = "openai"
cognee.config.embedding_model = "text-embedding-3-small"
```

### 5. Environment Variables

Use environment variables for production:

```bash
# .env file
GITHUB_TOKEN=your-token
LLM_PROVIDER=github_copilot
LLM_MODEL=gpt-4o
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small
LLM_API_KEY=your-openai-key
```

## Troubleshooting

### Issue: Authentication Errors

**Problem**: "Invalid token" or authentication failures

**Solution**:
```python
# Verify token is set correctly
import os
print(os.environ.get("GITHUB_TOKEN"))

# Or provide explicitly
register_github_copilot_adapters(api_key="your-token")
```

### Issue: Model Not Available

**Problem**: Model not accessible or quota exceeded

**Solution**:
- Check your Copilot plan (Pro+ or higher required for all models)
- Verify model name is correct
- Try a different model with lower multiplier

### Issue: Embedding Errors

**Problem**: "No embedding provider" error

**Solution**:
```python
# GitHub Copilot doesn't provide embeddings
# Configure separate embedding provider
cognee.config.embedding_provider = "openai"
cognee.config.embedding_model = "text-embedding-3-small"
```

### Issue: Rate Limiting

**Problem**: Too many requests

**Solution**:
```python
# Enable rate limiting
cognee.config.llm_rate_limit_enabled = True
cognee.config.llm_rate_limit_requests = 30  # Reduce request rate
cognee.config.llm_rate_limit_interval = 60
```

### Issue: Timeout Errors

**Problem**: Requests timing out

**Solution**:
- Use faster models (gpt-4o, gemini-2.0-flash)
- Reduce max_completion_tokens
- Implement retry logic

## Getting Help

- **Documentation**: See MODELS.md for complete model list
- **GitHub Issues**: Report bugs and issues
- **Discord**: Join Cognee community
- **Examples**: Check example.py for working code

## License

Apache-2.0
