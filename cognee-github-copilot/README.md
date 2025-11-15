# Cognee GitHub Copilot Adapter

External adapter package for integrating GitHub Copilot models with Cognee.

## Features

- **14+ LLM Models**: Support for ALL GitHub Copilot Pro+ models from OpenAI, Anthropic, Google, and xAI
- **Multi-Provider Access**: Access models from OpenAI (GPT-4.1, GPT-5, o3), Anthropic (Claude Opus/Sonnet), Google (Gemini), and xAI (Grok)
- **Flexible Authentication**: GitHub token-based authentication
- **Cross-Platform**: Works across GitHub.com, VS Code, Visual Studio, Eclipse, Xcode, and JetBrains IDEs
- **LiteLLM Integration**: Uses instructor[litellm] for structured outputs

## Installation

```bash
pip install -e cognee-github-copilot/
```

## Quick Start

```python
from cognee_github_copilot import register_github_copilot_adapters
import cognee

# Register GitHub Copilot adapters
register_github_copilot_adapters()

# Configure LLM
cognee.config.llm_provider = "github_copilot"
cognee.config.llm_model = "gpt-4o"

# Configure Embeddings (GitHub Copilot doesn't provide embeddings)
cognee.config.embedding_provider = "openai"
cognee.config.embedding_model = "text-embedding-3-small"

# Use Cognee as normal
await cognee.add("Your data here")
await cognee.cognify()
results = await cognee.search("your query")
```

## Supported Models

### OpenAI Models
- **GPT-4.1** - Advanced reasoning, 0x multiplier (included)
- **GPT-4o** - Fast, multimodal, 0x multiplier (included)
- **GPT-5** - Next-generation reasoning, 1x multiplier
- **GPT-5 mini** - Lightweight and fast, 0x multiplier (included)
- **o3** - Extended reasoning, 1x multiplier
- **o4-mini** - Balanced reasoning, 0.33x multiplier

### Anthropic Models
- **Claude Opus 4.1** - Highest capability, 10x multiplier
- **Claude Opus 4** - Top-tier reasoning, 10x multiplier
- **Claude Sonnet 3.5** - Balanced performance, 1x multiplier
- **Claude Sonnet 3.7** - Enhanced reasoning, 1x multiplier
- **Claude Sonnet 3.7 Thinking** - Visible reasoning, 1.25x multiplier
- **Claude Sonnet 4** - Latest balanced model, 1x multiplier

### Google Models
- **Gemini 2.5 Pro** - 1M+ context, 1x multiplier
- **Gemini 2.0 Flash** - Fast and efficient, 0.25x multiplier

### xAI Models
- **Grok Code Fast 1** - Code-optimized, 0.25x multiplier (complimentary until Sept 2025)

## Configuration Examples

### Basic Usage

```python
import cognee
from cognee_github_copilot import register_github_copilot_adapters

# Register GitHub Copilot
register_github_copilot_adapters()

# Use any supported model
cognee.config.llm_provider = "github_copilot"
cognee.config.llm_model = "claude-sonnet-4"  # or gpt-4o, gemini-2.5-pro, etc.
```

### With Custom API Key

```python
from cognee_github_copilot import register_github_copilot_adapters

register_github_copilot_adapters(
    api_key="your-github-token"
)
```

### Complete Example with All Configuration

```python
import cognee
from cognee_github_copilot import register_github_copilot_adapters

# Register GitHub Copilot
register_github_copilot_adapters(api_key="your-github-token")

# Configure LLM
cognee.config.llm_provider = "github_copilot"
cognee.config.llm_model = "gpt-4o"

# Configure Embeddings separately
cognee.config.embedding_provider = "openai"
cognee.config.embedding_model = "text-embedding-3-small"
cognee.config.embedding_dimensions = 1536

# Use Cognee
await cognee.add("Complex data about AI systems")
await cognee.cognify()
results = await cognee.search("How do AI systems work?")
```

## Environment Variables

```bash
# GitHub Token (optional, can be provided in code)
export GITHUB_TOKEN=your_github_token

# LLM Configuration
export LLM_PROVIDER=github_copilot
export LLM_MODEL=gpt-4o

# Embedding Configuration (separate provider required)
export EMBEDDING_PROVIDER=openai
export EMBEDDING_MODEL=text-embedding-3-small
export LLM_API_KEY=your_openai_api_key
```

## Model Selection Guide

### For Speed
- Gemini 2.0 Flash
- Grok Code Fast 1
- GPT-4o
- GPT-5 mini

### For Cost Efficiency
- GPT-4.1, GPT-4o, GPT-5 mini (0x multiplier)
- Gemini 2.0 Flash (0.25x)
- Grok Code Fast 1 (0.25x)

### For Maximum Capability
- Claude Opus 4.1
- Claude Opus 4
- GPT-5
- Claude Sonnet 4

### For Large Context
- Gemini 2.5 Pro (1M+ tokens)
- Gemini 2.0 Flash (1M tokens)
- Claude models (200K tokens)

### For Reasoning
- o3 (extended reasoning)
- Claude Sonnet 3.7 Thinking (visible reasoning)
- Claude Opus 4.1 (advanced reasoning)

## Important Notes

### No Embedding Support
GitHub Copilot does not provide embedding models. You must configure embeddings separately:

```python
# Configure embeddings with a different provider
cognee.config.embedding_provider = "openai"
cognee.config.embedding_model = "text-embedding-3-small"
```

Supported embedding providers:
- OpenAI (text-embedding-3-small, text-embedding-3-large)
- Cohere (embed-english-v3.0, embed-multilingual-v3.0)
- Any other provider supported by cognee

### Premium Request Multipliers
Each model has a multiplier that affects premium request consumption:
- **0x** (included): GPT-4.1, GPT-4o, GPT-5 mini
- **0.25x**: Gemini 2.0 Flash, Grok Code Fast 1
- **0.33x**: o4-mini
- **1x**: Most models (GPT-5, Claude Sonnet series, Gemini 2.5 Pro)
- **1.25x**: Claude Sonnet 3.7 Thinking
- **10x**: Claude Opus models (premium)

### Authentication
Uses `GITHUB_TOKEN` from environment by default. Override with custom API key:

```python
register_github_copilot_adapters(api_key="your-custom-token")
```

### Required Headers
The adapter automatically includes GitHub Copilot headers:
- `editor-version: vscode/1.85.1`
- `Copilot-Integration-Id: vscode-chat`

## Documentation

- **README.md** - This file, quick start and overview
- **docs/MODELS.md** - Complete model catalog with all 14+ models and configurations
- **docs/README.md** - Detailed usage guide

## Prerequisites

1. GitHub Copilot Pro+ subscription (or higher tier)
2. GitHub Personal Access Token with Copilot access
3. Active GitHub Copilot license
4. Python 3.10+

## Model Availability by Plan

| Plan | Models Available |
|------|------------------|
| **Copilot Free** | GPT-4.1, GPT-4o, GPT-5 mini, Claude Sonnet 3.5, Gemini 2.0 Flash |
| **Copilot Pro** | All 14+ models |
| **Copilot Pro+** | All 14+ models |
| **Copilot Business** | All 14+ models |
| **Copilot Enterprise** | All 14+ models |

## Supported Platforms

All models work across:
- ✓ GitHub.com
- ✓ Visual Studio Code
- ✓ Visual Studio
- ✓ Eclipse
- ✓ Xcode
- ✓ JetBrains IDEs

## Troubleshooting

### Authentication Errors
Ensure your `GITHUB_TOKEN` has Copilot access:
```bash
export GITHUB_TOKEN=your_github_token
```

### Model Not Available
Some models require Copilot Pro+ or higher. Check model availability in docs/MODELS.md.

### Embedding Errors
Remember: GitHub Copilot doesn't provide embeddings. Configure a separate embedding provider:
```python
cognee.config.embedding_provider = "openai"
cognee.config.embedding_model = "text-embedding-3-small"
```

## Contributing

Contributions are welcome! Please follow the standard cognee contribution guidelines.

## License

Apache-2.0

## Support

For issues and questions:
- GitHub Issues: https://github.com/topoteretes/cognee/issues
- Discord: https://discord.gg/NQPKmU5CCg
- Documentation: https://docs.cognee.ai
