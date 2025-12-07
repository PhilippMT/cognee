# AWS Bedrock BAML Documentation

Welcome to the documentation for the `cognee-aws-bedrock-baml` package.

**Last Updated: December 2025**

## Documentation Index

| Document | Description |
|----------|-------------|
| [Overview](./OVERVIEW.md) | Quick reference and what's new |
| [LLM Models](./LLM_MODELS.md) | Complete LLM model catalog (39+ models) |
| [Embedding Models](./EMBEDDING_MODELS.md) | Embedding model catalog (10 models) |
| [BAML Configuration](./BAML_CONFIG.md) | BAML client configuration examples |
| [Cross-Region](./CROSS_REGION.md) | Cross-region inference profiles |
| [Best Practices](./BEST_PRACTICES.md) | Usage recommendations |

## Quick Start

```python
from cognee_aws_bedrock_baml import (
    register_baml_bedrock_adapters,
    get_model_config,
    ALL_MODELS,
    EMBEDDING_MODELS,
)
import cognee

# Register adapters with cognee
register_baml_bedrock_adapters()

# Configure cognee
cognee.config.llm_provider = "aws_bedrock_baml"
cognee.config.llm_model = "bedrock/anthropic.claude-sonnet-4-5-20250929-v1:0"
cognee.config.embedding_model = "bedrock/amazon.titan-embed-text-v2:0"

# Use cognee normally
await cognee.add("Your data here")
await cognee.cognify()
results = await cognee.search("query")
```

## What's New (December 2025)

### New Model Providers
- **Qwen**: Qwen3 32B, 235B, Coder 30B/480B, VL 235B
- **OpenAI OSS**: GPT OSS 120B, 20B, Safeguard models
- **Google Gemma**: Gemma 3 4B, 12B, 27B IT models
- **NVIDIA**: Nemotron Nano 9B, 12B v2
- **DeepSeek**: V3.1
- **MiniMax**: M2
- **TwelveLabs**: Pegasus v1.2, Marengo Embed 2.7/3.0

### Updated Models
- **Anthropic Claude**: Claude 4.x series (Sonnet 4.5, Sonnet 4, Opus 4.5, Haiku 4.5, Claude 3.7 Sonnet)
- **Amazon Nova**: Nova 2 Lite with cross-region support
- **Mistral AI**: Pixtral Large, Ministral 3, Voxtral (audio-capable)
- **Cohere**: Embed v4 (multimodal)

## Support

For issues or questions, please refer to the main cognee repository documentation.
