# Cognee AWS Bedrock Adapter

External adapter package for integrating AWS Bedrock foundation models with Cognee.

## Features

- **20+ LLM Models**: Claude, Llama, Titan, Nova from Anthropic, Meta, and Amazon
- **7 Embedding Models**: Titan and Cohere embeddings with various dimensions
- **3 Reranking Models**: Cohere reranking models for improved search relevance
- **Cross-Region Inference**: Automatic load distribution across EU regions
- **Flexible Authentication**: AWS profiles, explicit credentials, or default chain
- **Separate Configurations**: Independent region and profile settings for LLM vs embeddings

## Installation

```bash
pip install -e cognee-aws-bedrock/
```

**Note:** This adapter now uses `instructor[bedrock]` for native AWS Bedrock integration instead of litellm. Embeddings still use litellm for compatibility.

## Quick Start

```python
from cognee_aws_bedrock import register_bedrock_adapters
import cognee

# Register AWS Bedrock adapters
register_bedrock_adapters()

# Configure LLM
cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
cognee.config.aws_region_name = "eu-central-1"
cognee.config.aws_profile_name = "my-profile"  # Optional

# Configure Embeddings
cognee.config.embedding_provider = "bedrock"
cognee.config.embedding_model = "bedrock/amazon.titan-embed-text-v2:0"
cognee.config.embedding_dimensions = 1024

# Use Cognee as normal
await cognee.add("Your data here")
await cognee.cognify()
```

## Advanced Configuration

### Separate AWS Regions and Profiles

```python
from cognee_aws_bedrock import register_bedrock_adapters

# Register with different regions and profiles for LLM vs embeddings
register_bedrock_adapters(
    llm_region="eu-west-1",
    llm_profile="my-llm-profile",
    embedding_region="eu-central-1",
    embedding_profile="my-embedding-profile"
)
```

### Cross-Region Inference

```python
import cognee

# Use cross-region inference profiles
cognee.config.llm_model = "bedrock/eu.anthropic.claude-3-7-sonnet-20250219-v1:0"
cognee.config.embedding_model = "bedrock/eu.cohere.embed-multilingual-v4:0"
```

## Supported Models

See `src/cognee_aws_bedrock/docs/MODELS.md` for a complete list of supported models and configuration examples.

### LLM Models (EU Regions)

- **Claude 3.7 Sonnet** - Latest, best performance
- **Claude 3.5 Sonnet v2** - Balanced performance/cost
- **Claude 3 Haiku** - Fast, cost-effective
- **Llama 3.1/3.2** - Open-source alternatives (8B-405B)
- **Amazon Titan** - AWS-native models
- **Amazon Nova** - Multimodal models

### Embedding Models

- **Amazon Titan Embed Text v1** - 1536 dimensions
- **Amazon Titan Embed Text v2** - 1024 dimensions (configurable)
- **Cohere Embed Multilingual v3** - 1024 dimensions, 100+ languages
- **Cohere Embed English v3** - 1024 dimensions
- **Cross-region profiles** - `eu.*` models

### Reranking Models

- **Cohere Rerank v3.5** - State-of-the-art multilingual
- **Cohere Rerank English v3** - English-optimized
- **Cohere Rerank Multilingual v3** - 100+ languages

## Environment Variables

```bash
# LLM Configuration
export LLM_PROVIDER=aws_bedrock
export LLM_MODEL=bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0
export AWS_REGION_NAME=eu-central-1
export AWS_PROFILE_NAME=my-profile

# Embedding Configuration
export EMBEDDING_PROVIDER=bedrock
export EMBEDDING_MODEL=bedrock/amazon.titan-embed-text-v2:0
export EMBEDDING_DIMENSIONS=1024
```

## Batching Support

AWS Bedrock supports batch processing for both LLMs and embeddings:

### LLM Batching

```python
# Bedrock supports batch inference for Anthropic models
# Configure via AWS Bedrock Batch API (separate from real-time inference)
# See: https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html
```

### Embedding Batching

```python
# Embeddings automatically batch requests up to model limits
# Titan Embed v2: Up to 8,192 tokens per request
# Cohere Embed: Automatic batching handled by litellm
```

## Prerequisites

1. AWS account with Bedrock access
2. Model access enabled in AWS Bedrock console (one-time setup per region)
3. IAM permissions:
   - `bedrock:InvokeModel`
   - `bedrock:InvokeModelWithResponseStream`
   - `bedrock:ListCrossRegionInferenceProfiles` (optional)
4. AWS credentials configured:
   - Named profile in `~/.aws/credentials` (recommended)
   - Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
   - IAM role (when running on EC2, ECS, Lambda, etc.)
5. Python dependencies:
   - `instructor[bedrock]>=1.0.0`
   - `boto3>=1.34.0`

## Documentation

- **README.md** - This file, quick start and overview
- **docs/MODELS.md** - Complete model catalog with configuration examples
- **docs/README.md** - Detailed usage guide
- **docs/IMPLEMENTATION_SUMMARY.md** - Technical implementation details

## License

MIT
