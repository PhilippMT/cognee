# AWS Bedrock BAML - Documentation Index

This directory contains comprehensive documentation for the AWS Bedrock BAML integration.

## Documentation Files

| File | Description |
|------|-------------|
| [OVERVIEW.md](OVERVIEW.md) | Quick reference and getting started guide |
| [BAML_CONFIG.md](BAML_CONFIG.md) | BAML client configuration examples |
| [LLM_MODELS.md](LLM_MODELS.md) | Complete LLM model catalog with specifications |
| [EMBEDDING_MODELS.md](EMBEDDING_MODELS.md) | Embedding model catalog and configuration |
| [CROSS_REGION.md](CROSS_REGION.md) | Cross-region inference profiles |
| [BEST_PRACTICES.md](BEST_PRACTICES.md) | Best practices and recommendations |

## Supported EU Regions

- **eu-central-1** (Frankfurt)
- **eu-west-1** (Ireland)
- **eu-north-1** (Stockholm)

## Model Providers

| Provider | LLM Models | Embedding Models |
|----------|------------|------------------|
| Anthropic | 5 (Claude 3.x) | - |
| Amazon | 6 (Nova, Titan) | 3 (Titan Embed) |
| Meta | 8 (Llama 3.x) | - |
| Mistral AI | 4 (Mistral, Mixtral) | - |
| Cohere | 2 (Command R) | 2 (Embed v3) |
| AI21 Labs | 4 (Jamba, Jurassic) | - |

**Total: 29 LLM models + 5 Embedding models**

## Quick Start

```python
from cognee_aws_bedrock_baml import register_baml_bedrock_adapters
import cognee

# Register adapters
register_baml_bedrock_adapters()

# Configure LLM
cognee.config.llm_provider = "aws_bedrock_baml"
cognee.config.llm_model = "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"

# Configure Embeddings
cognee.config.embedding_provider = "bedrock"
cognee.config.embedding_model = "bedrock/amazon.titan-embed-text-v2:0"
```

## References

- [BAML Documentation](https://docs.boundaryml.com/)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Cognee Documentation](https://docs.cognee.ai/)
