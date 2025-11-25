# Cognee AWS Bedrock BAML Adapter

External adapter package for integrating AWS Bedrock foundation models with Cognee using **BAML** (Boundary ML) for type-safe LLM interactions.

## What is BAML?

[BAML](https://docs.boundaryml.com/) is a domain-specific language for building AI applications with type-safe LLM interactions. It provides:
- Type-safe structured outputs
- Native AWS Bedrock support via the `aws-bedrock` provider
- Automatic JSON parsing and validation
- Configurable inference parameters

## Features

- **Native BAML Integration**: Uses BAML's `aws-bedrock` provider for type-safe structured outputs
- **30+ LLM Models**: Claude, Llama, Titan, Nova, Mistral, Cohere from Anthropic, Meta, Amazon, Mistral AI, and Cohere
- **Automatic Configuration**: Models properly configured with correct settings
- **Comprehensive Model Configuration**: All models from cognee-aws-bedrock are supported
- **7 Embedding Models**: Titan and Cohere embeddings with various dimensions
- **Cross-Region Inference**: Automatic load distribution across EU regions
- **Flexible Authentication**: AWS profiles, explicit credentials, or default chain
- **Separate Configurations**: Independent region and profile settings for LLM vs embeddings

## Installation

```bash
pip install -e cognee-aws-bedrock-baml/
```

This will automatically install:
- `baml-py>=0.214.0` (BAML Python client)
- `boto3>=1.34.0`
- `litellm>=1.0.0` (for embeddings)
- `cognee>=0.1.0`

## Quick Start

```python
from cognee_aws_bedrock_baml import register_baml_bedrock_adapters
import cognee

# Register AWS Bedrock BAML adapters
register_baml_bedrock_adapters()

# Configure LLM
cognee.config.llm_provider = "aws_bedrock_baml"
cognee.config.llm_model = "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"
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

## BAML Configuration

This package includes BAML configuration files in `baml_src/` directory:

### clients.baml

Defines all AWS Bedrock LLM clients:

```baml
// Claude 3.5 Sonnet v2 - Latest generation, best performance
client<llm> ClaudeSonnet35V2 {
  provider aws-bedrock
  options {
    model "anthropic.claude-3-5-sonnet-20241022-v2:0"
    inference_configuration {
      max_tokens 8192
      temperature 0.7
    }
  }
}
```

### generators.baml

Configures the BAML code generator:

```baml
generator py_client {
  output_type python/pydantic
  output_dir "../baml_client"
  version "0.214.0"
  default_client_mode sync
}
```

## Advanced Configuration

### Separate AWS Regions and Profiles

```python
from cognee_aws_bedrock_baml import register_baml_bedrock_adapters

# Register with different regions and profiles for LLM vs embeddings
register_baml_bedrock_adapters(
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
cognee.config.llm_model = "bedrock/eu.anthropic.claude-3-5-sonnet-20241022-v2:0"
cognee.config.embedding_model = "bedrock/eu.cohere.embed-multilingual-v4:0"
```

## Supported Models

See `docs/MODELS.md` for a complete list of **30+ supported models** with detailed configuration examples.

### LLM Models (EU Regions: eu-central-1, eu-north-1)

**Anthropic Claude (Tools Support):**
- **Claude 3.5 Sonnet v2** (`anthropic.claude-3-5-sonnet-20241022-v2:0`) - Latest, best performance
- **Claude 3.5 Haiku** (`anthropic.claude-3-5-haiku-20241022-v1:0`) - Fast, cost-effective
- **Claude 3 Sonnet/Haiku** - Established workloads

**Amazon Nova (Multimodal):**
- **Amazon Nova Pro/Lite/Micro** - Multimodal models (text, image, video)

**Meta Llama (Open Source):**
- **Llama 3.3 70B** (`meta.llama3-3-70b-instruct-v1:0`) - Latest open-source
- **Llama 3.2 Vision** - 90B and 11B models with image support
- **Llama 3.2 1B/3B** - Ultra-efficient edge models
- **Llama 3.1 405B/70B/8B** - Flexible scaling options

**Mistral AI (European):**
- **Mistral Large 2** (`mistral.mistral-large-2407-v1:0`) - Latest Mistral
- **Mixtral 8x7B** - Mixture of experts model

**Cohere (RAG Optimized):**
- **Cohere Command R+/R** - Optimized for RAG and search

**Amazon Titan (JSON Mode Only):**
- **Amazon Titan Text** (Premier, Express, Lite) - AWS-native models

### Embedding Models

- **Amazon Titan Embed Text v1** - 1536 dimensions
- **Amazon Titan Embed Text v2** - 1024 dimensions (configurable)
- **Cohere Embed Multilingual v3** - 1024 dimensions, 100+ languages
- **Cohere Embed English v3** - 1024 dimensions
- **Cross-region profiles** - `eu.*` models

## Environment Variables

```bash
# LLM Configuration
export LLM_PROVIDER=aws_bedrock_baml
export LLM_MODEL=bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0
export AWS_REGION=eu-central-1
export AWS_PROFILE=my-profile

# Embedding Configuration
export EMBEDDING_PROVIDER=bedrock
export EMBEDDING_MODEL=bedrock/amazon.titan-embed-text-v2:0
export EMBEDDING_DIMENSIONS=1024
```

## Comparison with cognee-aws-bedrock

| Feature | cognee-aws-bedrock | cognee-aws-bedrock-baml |
|---------|-------------------|-------------------------|
| LLM Framework | instructor[bedrock] | BAML |
| Structured Output | Instructor modes | BAML type system |
| Tools Support | BEDROCK_TOOLS mode | Native BAML support |
| JSON Fallback | BEDROCK_JSON mode | Automatic |
| Configuration | Python code | BAML DSL files |
| Type Safety | Pydantic | BAML + Pydantic |
| Embeddings | LiteLLM | LiteLLM |

## BAML vs Instructor

**BAML:**
- Domain-specific language for AI applications
- Type-safe structured outputs with validation
- Declarative client configuration in `.baml` files
- Automatic retry and error handling

**Instructor:**
- Python library for structured LLM outputs
- Uses Pydantic for validation
- Programmatic configuration
- Multiple mode support (tools, JSON, etc.)

Both approaches work well with AWS Bedrock. Choose based on your preferences:
- Use **cognee-aws-bedrock** if you prefer Python-centric configuration
- Use **cognee-aws-bedrock-baml** if you prefer declarative DSL configuration

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
- **baml_src/** - BAML configuration files

## References

- [BAML Documentation](https://docs.boundaryml.com/)
- [BAML AWS Bedrock Provider](https://docs.boundaryml.com/ref/llm-client-providers/aws-bedrock)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Cognee Documentation](https://docs.cognee.ai/)

## License

MIT
