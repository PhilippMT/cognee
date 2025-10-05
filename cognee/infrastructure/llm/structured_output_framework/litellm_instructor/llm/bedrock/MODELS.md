# AWS Bedrock Foundation Models Support

This document lists AWS Bedrock foundation models available in EU regions (eu-central-1, eu-north-1, eu-west-1) with cross-region inference support.

## Supported Models

### Anthropic Claude Models

#### Claude 3.7 Sonnet
- **Model ID**: `anthropic.claude-3-7-sonnet-20250219-v1:0`
- **LiteLLM ID**: `bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0`
- **Cross-Region ID**: `bedrock/eu.anthropic.claude-3-7-sonnet-20250219-v1:0`
- **Regions**: eu-central-1, eu-north-1, eu-west-1, eu-west-2, eu-west-3
- **Capabilities**: Text, Image input | Text, Chat output
- **Status**: Generally Available (Released: Feb 24, 2025)

#### Claude 3.5 Sonnet v2
- **Model ID**: `anthropic.claude-3-5-sonnet-20241022-v2:0`
- **LiteLLM ID**: `bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0`
- **Regions**: eu-central-1, eu-west-1 (check AWS console for availability)
- **Capabilities**: Text, Image input | Text, Chat output
- **Status**: Generally Available (Released: Oct 22, 2024)

#### Claude 3.5 Sonnet v1
- **Model ID**: `anthropic.claude-3-5-sonnet-20240620-v1:0`
- **LiteLLM ID**: `bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0`
- **Regions**: Multiple EU regions
- **Capabilities**: Text, Image input | Text, Chat output
- **Status**: Generally Available (Released: July 30, 2024)

#### Claude 3 Sonnet
- **Model ID**: `anthropic.claude-3-sonnet-20240229-v1:0`
- **LiteLLM ID**: `bedrock/anthropic.claude-3-sonnet-20240229-v1:0`
- **Regions**: eu-central-1, eu-west-1, eu-west-2, eu-west-3
- **Capabilities**: Text, Image input | Text, Chat output
- **Status**: Generally Available

#### Claude 3 Haiku
- **Model ID**: `anthropic.claude-3-haiku-20240307-v1:0`
- **LiteLLM ID**: `bedrock/anthropic.claude-3-haiku-20240307-v1:0`
- **Regions**: eu-central-1, eu-west-1, eu-west-2, eu-west-3
- **Capabilities**: Text, Image input | Text, Chat output
- **Status**: Generally Available

### Meta Llama Models

#### Llama 3.2 Models
- **Model IDs**: 
  - `meta.llama-3-2-1b-instruct-v1:0` (1B parameters)
  - `meta.llama-3-2-3b-instruct-v1:0` (3B parameters)
  - `meta.llama-3-2-11b-instruct-v1:0` (11B Vision)
  - `meta.llama-3-2-90b-instruct-v1:0` (90B Vision)
- **LiteLLM ID**: `bedrock/meta.llama-3-2-*-instruct-v1:0`
- **Status**: Generally Available (Released: Sept 2024)

#### Llama 3.1 Models
- **Model IDs**:
  - `meta.llama-3-1-8b-instruct-v1:0` (8B parameters)
  - `meta.llama-3-1-70b-instruct-v1:0` (70B parameters)
  - `meta.llama-3-1-405b-instruct-v1:0` (405B parameters)
- **LiteLLM ID**: `bedrock/meta.llama-3-1-*-instruct-v1:0`
- **Status**: Generally Available

### Amazon Titan Models

#### Titan Text Models
- **Model IDs**:
  - `amazon.titan-text-premier-v1:0` (Premier)
  - `amazon.titan-text-express-v1` (Express)
  - `amazon.titan-text-lite-v1` (Lite)
- **LiteLLM ID**: `bedrock/amazon.titan-text-*`
- **Status**: Generally Available

#### Titan Embeddings Models
- **Model IDs**:
  - `amazon.titan-embed-text-v1` (Text Embeddings G1)
  - `amazon.titan-embed-text-v2:0` (Text Embeddings V2)
  - `amazon.titan-embed-image-v1` (Multimodal Embeddings G1)
- **LiteLLM ID**: `bedrock/amazon.titan-embed-*`
- **Status**: Generally Available

#### Titan Image Generator
- **Model ID**: `amazon.titan-image-generator-v1`
- **LiteLLM ID**: `bedrock/amazon.titan-image-generator-v1`
- **Status**: Generally Available

### Amazon Nova Models

#### Nova Text Models
- **Model IDs**:
  - `amazon.nova-micro-v1:0` (Micro)
  - `amazon.nova-lite-v1:0` (Lite)
  - `amazon.nova-pro-v1:0` (Pro)
- **LiteLLM ID**: `bedrock/amazon.nova-*-v1:0`
- **Status**: Generally Available (Launched late 2024)

#### Nova Multimodal Models
- **Model IDs**:
  - `amazon.nova-canvas-v1:0` (Image generation)
  - `amazon.nova-reel-v1:1` (Video generation)
  - `amazon.nova-sonic-v1:0` (Audio)
- **Status**: Generally Available

## Cross-Region Inference

AWS Bedrock supports cross-region inference, which allows you to manage unplanned traffic bursts by utilizing compute across different AWS regions. This feature provides:

1. **Higher Throughput**: Distribute traffic across multiple regions automatically
2. **Better Availability**: Seamless failover if capacity is limited in one region
3. **Simplified Management**: Use a single inference profile ID instead of managing multiple regional endpoints

### Cross-Region Inference Profiles

For EU regions, use the following prefixes:

- **EU Cross-Region Profile**: `eu.<model-id>`
  - Example: `eu.anthropic.claude-3-7-sonnet-20250219-v1:0`
  - Destination Regions: eu-central-1, eu-north-1, eu-west-1, eu-west-2, eu-west-3

### Using Cross-Region Inference with Cognee

To use cross-region inference profiles, prefix your model with `bedrock/` and use the cross-region profile ID:

```python
import cognee

# Configure AWS Bedrock with cross-region inference
cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/eu.anthropic.claude-3-7-sonnet-20250219-v1:0"
cognee.config.aws_region_name = "eu-central-1"  # Source region
cognee.config.aws_access_key_id = "YOUR_AWS_ACCESS_KEY_ID"
cognee.config.aws_secret_access_key = "YOUR_AWS_SECRET_ACCESS_KEY"
```

Or use direct model IDs:

```python
cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
cognee.config.aws_region_name = "eu-west-1"
```

## Configuration

### Environment Variables

Set these environment variables to use AWS Bedrock:

```bash
LLM_PROVIDER=aws_bedrock
LLM_MODEL=bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0
AWS_REGION_NAME=eu-central-1
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
```

### Using Default AWS Credentials

If you have AWS credentials configured via `aws configure` or IAM roles, you can omit the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`:

```bash
LLM_PROVIDER=aws_bedrock
LLM_MODEL=bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0
AWS_REGION_NAME=eu-central-1
```

### BAML Configuration

For BAML framework support, configure in your code:

```python
from cognee.infrastructure.llm import get_llm_config

config = get_llm_config()
config.baml_llm_provider = "aws-bedrock"
config.baml_llm_model = "anthropic.claude-3-7-sonnet-20250219-v1:0"
config.baml_llm_endpoint = "eu-central-1"  # Region as endpoint
```

## Model Selection Guidelines

### For General Purpose Tasks
- **Claude 3.7 Sonnet**: Best overall performance, latest features
- **Claude 3.5 Sonnet v2**: Excellent balance of performance and cost
- **Llama 3.1 70B**: Open-source alternative with strong capabilities

### For Cost Optimization
- **Claude 3 Haiku**: Fast, cost-effective for simpler tasks
- **Llama 3.2 3B/1B**: Ultra-compact for lightweight tasks
- **Amazon Titan Text Lite**: AWS-native, cost-effective option

### For Specialized Tasks
- **Llama 3.2 Vision models**: Multi-modal understanding
- **Amazon Nova Canvas/Reel**: Image and video generation
- **Amazon Titan Embeddings**: Text embeddings for RAG/search

## References

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [AWS Bedrock Cross-Region Inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)
- [LiteLLM AWS Bedrock Provider](https://docs.litellm.ai/docs/providers/bedrock)
- [AWS Bedrock Model Support by Region](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)
