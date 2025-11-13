# Cognee AWS Bedrock Adapter

External adapter package for integrating AWS Bedrock foundation models with Cognee using **instructor[bedrock]** for native tools/function calling support.

## Features

- **Native Bedrock Integration**: Uses instructor[bedrock] for proper tools/function calling support
- **30+ LLM Models**: Claude, Llama, Titan, Nova, Mistral, Cohere from Anthropic, Meta, Amazon, Mistral AI, and Cohere
- **Automatic Mode Selection**: BEDROCK_TOOLS for models with function calling, BEDROCK_JSON for others
- **Comprehensive Model Configuration**: All models properly configured with correct settings
- **7 Embedding Models**: Titan and Cohere embeddings with various dimensions
- **3 Reranking Models**: Cohere reranking models for improved search relevance
- **Cross-Region Inference**: Automatic load distribution across EU regions
- **Flexible Authentication**: AWS profiles, explicit credentials, or default chain
- **Separate Configurations**: Independent region and profile settings for LLM vs embeddings

## Installation

```bash
pip install -e cognee-aws-bedrock/
```

This will automatically install:
- `instructor[bedrock]>=1.13.0` (includes boto3 and Anthropic SDK)
- `boto3>=1.34.0`
- `cognee>=0.1.0`

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

See `docs/MODELS.md` for a complete list of **30+ supported models** with detailed configuration examples.

### LLM Models (EU Regions: eu-central-1, eu-north-1)

**With Tools/Function Calling Support (BEDROCK_TOOLS mode):**

- **Claude 3.5 Sonnet v2** (`anthropic.claude-3-5-sonnet-20241022-v2:0`) - Latest, best performance
- **Claude 3.5 Haiku** (`anthropic.claude-3-5-haiku-20241022-v1:0`) - Fast, cost-effective
- **Amazon Nova Pro/Lite/Micro** - Multimodal models (text, image, video)
- **Llama 3.3 70B** (`meta.llama3-3-70b-instruct-v1:0`) - Latest open-source
- **Llama 3.2 Vision** - 90B and 11B models with image support
- **Llama 3.2 1B/3B** - Ultra-efficient edge models
- **Llama 3.1 405B/70B/8B** - Flexible scaling options
- **Mistral Large 2** (`mistral.mistral-large-2407-v1:0`) - Latest Mistral
- **Mixtral 8x7B** - Mixture of experts model
- **Cohere Command R+/R** - Optimized for RAG and search

**JSON Mode Only (BEDROCK_JSON):**
- **Amazon Titan Text** (Premier, Express, Lite) - AWS-native models

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

## Documentation

- **README.md** - This file, quick start and overview
- **docs/MODELS.md** - Complete model catalog with configuration examples
- **docs/README.md** - Detailed usage guide
- **docs/IMPLEMENTATION_SUMMARY.md** - Technical implementation details

## License

MIT
