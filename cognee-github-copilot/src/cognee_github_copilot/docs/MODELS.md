# GitHub Copilot Foundation Models Support

This document lists ALL GitHub Copilot Pro+ models available across different providers with complete configuration examples.

## Overview

GitHub Copilot Pro+ provides access to frontier models from multiple providers through a unified API. All models support:
- Text generation and chat
- Agent mode for autonomous coding
- Integration across GitHub.com, VS Code, Visual Studio, Eclipse, Xcode, and JetBrains IDEs

## Supported Model Providers

### OpenAI Models

#### GPT-4.1
- **Model ID**: `gpt-4.1`
- **LiteLLM ID**: `github_copilot/gpt-4.1`
- **Provider**: OpenAI
- **Status**: Generally Available (GA)
- **Features**: Advanced reasoning, code generation, multimodal (text + images)
- **Context Window**: 128K tokens
- **Best For**: Complex coding tasks, architecture design, debugging
- **Multiplier**: 0 (included in base plan)

#### GPT-4o
- **Model ID**: `gpt-4o`
- **LiteLLM ID**: `github_copilot/gpt-4o`
- **Provider**: OpenAI
- **Status**: Generally Available (GA)
- **Features**: Optimized for speed, multimodal (text + images + audio)
- **Context Window**: 128K tokens
- **Best For**: Fast responses, real-time coding assistance
- **Multiplier**: 0 (included in base plan)

#### GPT-5
- **Model ID**: `gpt-5`
- **LiteLLM ID**: `github_copilot/gpt-5`
- **Provider**: OpenAI
- **Status**: Public Preview
- **Features**: Next-generation reasoning, improved code understanding
- **Context Window**: 128K+ tokens
- **Best For**: Advanced problem-solving, complex refactoring
- **Multiplier**: 1

#### GPT-5 mini
- **Model ID**: `gpt-5-mini`
- **LiteLLM ID**: `github_copilot/gpt-5-mini`
- **Provider**: OpenAI
- **Status**: Public Preview
- **Features**: Lightweight, fast, cost-effective
- **Context Window**: 128K tokens
- **Best For**: Quick completions, inline suggestions, simple tasks
- **Multiplier**: 0 (included in base plan)

#### o3
- **Model ID**: `o3`
- **LiteLLM ID**: `github_copilot/o3`
- **Provider**: OpenAI
- **Status**: Public Preview
- **Features**: Advanced reasoning, chain-of-thought processing
- **Context Window**: Variable
- **Best For**: Complex algorithmic problems, mathematical reasoning
- **Multiplier**: 1
- **Note**: Slower but more thorough reasoning

#### o4-mini
- **Model ID**: `o4-mini`
- **LiteLLM ID**: `github_copilot/o4-mini`
- **Provider**: OpenAI
- **Status**: Public Preview
- **Features**: Balanced reasoning and speed
- **Context Window**: Variable
- **Best For**: Moderate complexity reasoning tasks
- **Multiplier**: 0.33

### Anthropic Models

#### Claude Opus 4.1
- **Model ID**: `claude-opus-4.1`
- **LiteLLM ID**: `github_copilot/claude-opus-4.1`
- **Provider**: Anthropic
- **Status**: Public Preview
- **Features**: Highest capability, advanced reasoning, multimodal
- **Context Window**: 200K tokens
- **Best For**: Most complex tasks, large codebases, architecture planning
- **Multiplier**: 10 (premium)
- **Note**: Most expensive but most capable

#### Claude Opus 4
- **Model ID**: `claude-opus-4`
- **LiteLLM ID**: `github_copilot/claude-opus-4`
- **Provider**: Anthropic
- **Status**: Generally Available (GA)
- **Features**: Top-tier reasoning, comprehensive code understanding
- **Context Window**: 200K tokens
- **Best For**: Complex refactoring, system design, code review
- **Multiplier**: 10 (premium)

#### Claude Sonnet 3.5
- **Model ID**: `claude-sonnet-3.5`
- **LiteLLM ID**: `github_copilot/claude-sonnet-3.5`
- **Provider**: Anthropic
- **Status**: Generally Available (GA)
- **Features**: Balanced performance and cost, good reasoning
- **Context Window**: 200K tokens
- **Best For**: General-purpose coding, balanced workloads
- **Multiplier**: 1

#### Claude Sonnet 3.7
- **Model ID**: `claude-sonnet-3.7`
- **LiteLLM ID**: `github_copilot/claude-sonnet-3.7`
- **Provider**: Anthropic
- **Status**: Generally Available (GA)
- **Features**: Enhanced reasoning, improved code generation
- **Context Window**: 200K tokens
- **Best For**: Standard development tasks, code completion
- **Multiplier**: 1

#### Claude Sonnet 3.7 Thinking
- **Model ID**: `claude-sonnet-3.7-thinking`
- **LiteLLM ID**: `github_copilot/claude-sonnet-3.7-thinking`
- **Provider**: Anthropic
- **Status**: Generally Available (GA)
- **Features**: Extended reasoning mode, step-by-step thinking
- **Context Window**: 200K tokens
- **Best For**: Complex problem-solving with visible reasoning steps
- **Multiplier**: 1.25
- **Note**: Shows reasoning process before final answer

#### Claude Sonnet 4
- **Model ID**: `claude-sonnet-4`
- **LiteLLM ID**: `github_copilot/claude-sonnet-4`
- **Provider**: Anthropic
- **Status**: Generally Available (GA)
- **Features**: Latest balanced model, improved performance
- **Context Window**: 200K tokens
- **Best For**: Modern development workflows, balanced needs
- **Multiplier**: 1

### Google Models

#### Gemini 2.5 Pro
- **Model ID**: `gemini-2.5-pro`
- **LiteLLM ID**: `github_copilot/gemini-2.5-pro`
- **Provider**: Google
- **Status**: Generally Available (GA)
- **Features**: Advanced multimodal, long context, reasoning
- **Context Window**: 1M+ tokens
- **Best For**: Large codebase analysis, documentation generation
- **Multiplier**: 1
- **Note**: Exceptional context window size

#### Gemini 2.0 Flash
- **Model ID**: `gemini-2.0-flash`
- **LiteLLM ID**: `github_copilot/gemini-2.0-flash`
- **Provider**: Google
- **Status**: Generally Available (GA)
- **Features**: Fast, efficient, good for real-time tasks
- **Context Window**: 1M tokens
- **Best For**: Quick completions, real-time assistance, streaming
- **Multiplier**: 0.25
- **Note**: Excellent speed-to-capability ratio

### xAI Models

#### Grok Code Fast 1
- **Model ID**: `grok-code-fast-1`
- **LiteLLM ID**: `github_copilot/grok-code-fast-1`
- **Provider**: xAI
- **Status**: Public Preview
- **Features**: Optimized for code, fast responses
- **Context Window**: Variable
- **Best For**: Code-specific tasks, quick iterations
- **Multiplier**: 0.25
- **Note**: Complimentary access until Sept 2, 2025

## Model Availability by Plan

| Model | Copilot Free | Copilot Pro | Copilot Pro+ | Copilot Business | Copilot Enterprise |
|-------|--------------|-------------|--------------|------------------|-------------------|
| GPT-4.1 | ✓ | ✓ | ✓ | ✓ | ✓ |
| GPT-4o | ✓ | ✓ | ✓ | ✓ | ✓ |
| GPT-5 mini | ✓ | ✓ | ✓ | ✓ | ✓ |
| GPT-5 | - | ✓ | ✓ | ✓ | ✓ |
| o3 | - | ✓ | ✓ | ✓ | ✓ |
| o4-mini | - | ✓ | ✓ | ✓ | ✓ |
| Claude Opus 4.1 | - | ✓ | ✓ | ✓ | ✓ |
| Claude Opus 4 | - | ✓ | ✓ | ✓ | ✓ |
| Claude Sonnet 3.5 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Claude Sonnet 3.7 | - | ✓ | ✓ | ✓ | ✓ |
| Claude Sonnet 3.7 Thinking | - | ✓ | ✓ | ✓ | ✓ |
| Claude Sonnet 4 | - | ✓ | ✓ | ✓ | ✓ |
| Gemini 2.5 Pro | - | ✓ | ✓ | ✓ | ✓ |
| Gemini 2.0 Flash | ✓ | ✓ | ✓ | ✓ | ✓ |
| Grok Code Fast 1 | - | ✓ | ✓ | ✓ | ✓ |

## Model Availability by Client

All models listed above are available across:
- ✓ GitHub.com
- ✓ Visual Studio Code
- ✓ Visual Studio
- ✓ Eclipse
- ✓ Xcode
- ✓ JetBrains IDEs

## Configuration Examples

### Basic Configuration

```python
import cognee
from cognee_github_copilot import register_github_copilot_adapters

# Register GitHub Copilot
register_github_copilot_adapters()

# Configure LLM
cognee.config.llm_provider = "github_copilot"
cognee.config.llm_model = "gpt-4o"  # or any model from the list
```

### All Model Configurations

#### OpenAI Models
```python
# GPT-4.1
cognee.config.llm_model = "gpt-4.1"

# GPT-4o
cognee.config.llm_model = "gpt-4o"

# GPT-5
cognee.config.llm_model = "gpt-5"

# GPT-5 mini
cognee.config.llm_model = "gpt-5-mini"

# o3
cognee.config.llm_model = "o3"

# o4-mini
cognee.config.llm_model = "o4-mini"
```

#### Anthropic Models
```python
# Claude Opus 4.1
cognee.config.llm_model = "claude-opus-4.1"

# Claude Opus 4
cognee.config.llm_model = "claude-opus-4"

# Claude Sonnet 3.5
cognee.config.llm_model = "claude-sonnet-3.5"

# Claude Sonnet 3.7
cognee.config.llm_model = "claude-sonnet-3.7"

# Claude Sonnet 3.7 Thinking
cognee.config.llm_model = "claude-sonnet-3.7-thinking"

# Claude Sonnet 4
cognee.config.llm_model = "claude-sonnet-4"
```

#### Google Models
```python
# Gemini 2.5 Pro
cognee.config.llm_model = "gemini-2.5-pro"

# Gemini 2.0 Flash
cognee.config.llm_model = "gemini-2.0-flash"
```

#### xAI Models
```python
# Grok Code Fast 1
cognee.config.llm_model = "grok-code-fast-1"
```

### With Custom API Key

```python
from cognee_github_copilot import register_github_copilot_adapters

register_github_copilot_adapters(
    api_key="your-github-token"
)
```

### Complete Example with Embeddings

```python
import cognee
from cognee_github_copilot import register_github_copilot_adapters

# Register GitHub Copilot for LLM
register_github_copilot_adapters()
cognee.config.llm_provider = "github_copilot"
cognee.config.llm_model = "claude-sonnet-4"

# Configure embeddings separately (GitHub Copilot doesn't provide embeddings)
cognee.config.embedding_provider = "openai"
cognee.config.embedding_model = "text-embedding-3-small"
cognee.config.embedding_dimensions = 1536

# Use Cognee as normal
await cognee.add("Your data here")
await cognee.cognify()
results = await cognee.search("query")
```

## Environment Variables

```bash
# GitHub Copilot API Key (optional, can be provided in code)
export GITHUB_TOKEN=your_github_token

# LLM Configuration
export LLM_PROVIDER=github_copilot
export LLM_MODEL=gpt-4o

# Embedding Configuration (separate from GitHub Copilot)
export EMBEDDING_PROVIDER=openai
export EMBEDDING_MODEL=text-embedding-3-small
export LLM_API_KEY=your_openai_api_key
```

## Model Selection Guide

### For Speed (Lowest Latency)
1. Gemini 2.0 Flash (0.25x multiplier)
2. Grok Code Fast 1 (0.25x multiplier)
3. GPT-4o (0x multiplier)
4. GPT-5 mini (0x multiplier)

### For Cost Efficiency
1. GPT-4.1 (0x multiplier)
2. GPT-4o (0x multiplier)
3. GPT-5 mini (0x multiplier)
4. Gemini 2.0 Flash (0.25x multiplier)
5. o4-mini (0.33x multiplier)

### For Maximum Capability
1. Claude Opus 4.1 (10x multiplier)
2. Claude Opus 4 (10x multiplier)
3. GPT-5 (1x multiplier)
4. Claude Sonnet 4 (1x multiplier)
5. Gemini 2.5 Pro (1x multiplier)

### For Reasoning Tasks
1. o3 (extended reasoning)
2. Claude Sonnet 3.7 Thinking (visible reasoning)
3. Claude Opus 4.1 (advanced reasoning)
4. GPT-5 (improved reasoning)

### For Large Context
1. Gemini 2.5 Pro (1M+ tokens)
2. Gemini 2.0 Flash (1M tokens)
3. Claude models (200K tokens)
4. GPT models (128K tokens)

## Important Notes

1. **No Embedding Support**: GitHub Copilot does not provide embedding models. You must configure embeddings separately using providers like OpenAI, Cohere, or others.

2. **Model Multipliers**: Premium request allowance is deducted according to model multipliers. Higher multipliers mean more premium requests consumed per API call.

3. **Model Availability**: All models are available in Copilot Pro+ and higher plans. Copilot Free has limited model access.

4. **Public Preview Models**: Models in public preview (GPT-5, GPT-5 mini, o3, o4-mini, Claude Opus 4.1, Grok Code Fast 1) may change or be replaced over time.

5. **Special Headers**: The adapter automatically includes required headers:
   - `editor-version: vscode/1.85.1`
   - `Copilot-Integration-Id: vscode-chat`

6. **Authentication**: Uses GITHUB_TOKEN from environment by default. Can be overridden with custom API key.

## Model Retirement Notice

Some models may be retired and replaced with newer versions. Always refer to GitHub's official documentation for the latest model availability.

Recent retirements (as of late 2025):
- Claude Sonnet 3.5 → Claude Haiku 4.5 (suggested alternative)
- Claude Opus 4 → Claude Opus 4.1
- Gemini 2.0 Flash → Gemini 2.5 Pro
- o1-mini, o3-mini, o4-mini → GPT-5 mini

## License

Apache-2.0
