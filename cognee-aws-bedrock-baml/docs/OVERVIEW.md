# AWS Bedrock BAML Integration - Overview

Quick reference for the cognee-aws-bedrock-baml package.

**Last Updated: December 2025**

## What's New

- **Claude 4.x Series**: Sonnet 4.5, Sonnet 4, Opus 4.5, Haiku 4.5, Claude 3.7 Sonnet
- **Amazon Nova 2**: Nova 2 Lite with improved multimodal capabilities
- **Qwen3 Models**: Including Qwen3 Coder 480B for code generation
- **OpenAI OSS**: GPT OSS 120B and 20B models
- **Google Gemma 3**: 4B, 12B, and 27B models
- **NVIDIA Nemotron**: Nano 9B and 12B models
- **DeepSeek V3.1**: Available in eu-north-1
- **Mistral Pixtral/Voxtral**: Multimodal and audio-capable models
- **Cohere Embed v4**: Multimodal embeddings (text + image)
- **TwelveLabs Marengo**: Video/audio embeddings

## Quick Stats

| Category | Count |
|----------|-------|
| LLM Models | 39+ |
| Embedding Models | 10 |
| Providers | 11 |
| EU Regions | 3 |

## Supported Providers

- **Anthropic**: Claude 4.x, 3.7, 3.5, 3.x
- **Amazon**: Nova 2, Nova Pro/Lite/Micro
- **Meta**: Llama 3.2
- **Mistral AI**: Pixtral, Ministral, Voxtral, Mistral, Mixtral
- **Qwen**: Qwen3, Qwen3 Coder, Qwen3 VL
- **OpenAI**: GPT OSS models
- **DeepSeek**: DeepSeek V3.1
- **Google**: Gemma 3 models
- **NVIDIA**: Nemotron Nano
- **MiniMax**: M2
- **TwelveLabs**: Pegasus, Marengo

## Quick Start

```python
from cognee_aws_bedrock_baml import (
    register_baml_bedrock_adapters,
    BamlBedrockLLMAdapter,
    BamlBedrockEmbeddingAdapter,
)
import cognee

# Register adapters
register_baml_bedrock_adapters()

# Configure cognee
cognee.config.llm_provider = "aws_bedrock_baml"
cognee.config.llm_model = "bedrock/anthropic.claude-sonnet-4-5-20250929-v1:0"
cognee.config.embedding_model = "bedrock/amazon.titan-embed-text-v2:0"
```

## Model Capabilities

### Multimodal Input
- **Text + Image**: Claude, Nova, Gemma, NVIDIA Nemotron, Qwen VL, Pixtral
- **Text + Video**: Nova, Pegasus
- **Text + Audio**: Voxtral models

### Large Context Windows
- **300K tokens**: Nova 2 Lite, Nova Pro, Nova Lite
- **200K tokens**: All Claude models
- **128K tokens**: Most other models

### All Models Support
- ✅ Tool/Function calling
- ✅ Streaming responses
- ✅ BAML structured outputs

## Documentation

- [LLM Models](./LLM_MODELS.md) - Complete LLM catalog
- [Embedding Models](./EMBEDDING_MODELS.md) - Embedding catalog
- [BAML Configuration](./BAML_CONFIG.md) - BAML setup
- [Cross-Region](./CROSS_REGION.md) - Cross-region inference
- [Best Practices](./BEST_PRACTICES.md) - Usage recommendations
