# AWS Bedrock Integration for Cognee

This directory contains the AWS Bedrock adapter for Cognee's LLM infrastructure, supporting both litellm_instructor and BAML frameworks.

## Overview

AWS Bedrock provides access to foundation models from leading AI companies including Anthropic, Meta, Amazon, and others through a unified, fully managed API. This integration enables Cognee to use AWS Bedrock models with support for:

- Multiple foundation model providers (Claude, Llama, Titan, Nova, etc.)
- Cross-region inference for higher throughput and availability
- EU region support (eu-central-1, eu-north-1, eu-west-1)
- Structured output generation via litellm and BAML
- AWS IAM authentication and credentials management

## Quick Start

### Using litellm_instructor (Default)

Configure via environment variables:

```bash
# Set provider and model
export LLM_PROVIDER=aws_bedrock
export LLM_MODEL=bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0

# Configure AWS region and credentials
export AWS_REGION_NAME=eu-central-1
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
```

Or configure programmatically:

```python
import cognee

cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
cognee.config.aws_region_name = "eu-central-1"
cognee.config.aws_access_key_id = "your_access_key"
cognee.config.aws_secret_access_key = "your_secret_key"
```

### Using BAML Framework

Configure via environment variables:

```bash
# Set structured output framework
export STRUCTURED_OUTPUT_FRAMEWORK=baml

# Set BAML provider and model
export BAML_LLM_PROVIDER=aws_bedrock
export BAML_LLM_MODEL=anthropic.claude-3-7-sonnet-20250219-v1:0
export BAML_LLM_ENDPOINT=eu-central-1  # Region as endpoint for BAML
```

Or configure programmatically:

```python
import cognee

cognee.config.structured_output_framework = "baml"
cognee.config.baml_llm_provider = "aws_bedrock"
cognee.config.baml_llm_model = "anthropic.claude-3-7-sonnet-20250219-v1:0"
cognee.config.baml_llm_endpoint = "eu-central-1"
```

### Using AWS Named Profile

You can use AWS named profiles from `~/.aws/credentials`:

**Environment Variable:**
```bash
export LLM_PROVIDER=aws_bedrock
export LLM_MODEL=bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0
export AWS_PROFILE_NAME=my-profile
export AWS_REGION_NAME=eu-central-1
```

**Python Code:**
```python
import cognee

cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
cognee.config.aws_profile_name = "my-profile"
cognee.config.aws_region_name = "eu-central-1"
```

## AWS Bedrock Embeddings

AWS Bedrock also supports embedding models for vector search and RAG applications.

### Supported Embedding Models

- **Amazon Titan Embed Text v2** (`bedrock/amazon.titan-embed-text-v2:0`) - 1024 dimensions
- **Amazon Titan Embed Text v1** (`bedrock/amazon.titan-embed-text-v1`) - 1536 dimensions
- **Amazon Titan Embed Image v1** (`bedrock/amazon.titan-embed-image-v1`) - Multimodal embeddings
- **Cohere Embed English v3** (`bedrock/cohere.embed-english-v3`)
- **Cohere Embed Multilingual v3** (`bedrock/cohere.embed-multilingual-v3`)

### Configuration

**Environment Variables:**
```bash
export EMBEDDING_PROVIDER=bedrock
export EMBEDDING_MODEL=bedrock/amazon.titan-embed-text-v2:0
export EMBEDDING_DIMENSIONS=1024
export AWS_REGION_NAME=eu-central-1
export AWS_PROFILE_NAME=my-profile  # Optional
```

**Python Code:**
```python
import cognee

cognee.config.embedding_provider = "bedrock"
cognee.config.embedding_model = "bedrock/amazon.titan-embed-text-v2:0"
cognee.config.embedding_dimensions = 1024
cognee.config.aws_region_name = "eu-central-1"
cognee.config.aws_profile_name = "my-profile"  # Optional
```

### Cross-Region Embedding Profiles

You can also use cross-region inference profiles for embeddings:

```python
cognee.config.embedding_model = "bedrock/eu.cohere.embed-multilingual-v4:0"
```

## AWS Bedrock Reranking

AWS Bedrock provides reranker models to improve the relevance of query responses by reordering search results.

### Supported Reranker Models

- **Cohere Rerank v3.5** (`cohere.rerank-v3-5:0`)
- **Cohere Rerank English v3** (`cohere.rerank-english-v3:0`)
- **Cohere Rerank Multilingual v3** (`cohere.rerank-multilingual-v3:0`)

### Usage

AWS Bedrock reranking is primarily used through the Knowledge Bases API for improved RAG (Retrieval-Augmented Generation) applications. The reranker models are integrated into the retrieval pipeline to reorder search results based on relevance to the query.

**Note**: AWS Bedrock reranking requires access to the Bedrock Knowledge Bases API and is configured at the knowledge base level. It is not directly invoked through litellm but can be used in conjunction with Cognee's search and retrieval pipelines.

For more information, see:
- [AWS Bedrock Reranking Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/rerank.html)
- [AWS Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)

## Cross-Region Inference

AWS Bedrock supports cross-region inference, which automatically routes requests across multiple regions for higher throughput and availability.

### Using Cross-Region Inference Profiles

For EU regions, use the `eu.` prefix:

```python
import cognee

cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/eu.anthropic.claude-3-7-sonnet-20250219-v1:0"
cognee.config.aws_region_name = "eu-central-1"  # Source region
```

Available cross-region profiles:
- `eu.*` - Routes across eu-central-1, eu-north-1, eu-west-1, eu-west-2, eu-west-3
- `us.*` - Routes across US regions
- `global.*` - Routes across all commercial AWS regions (limited models)

### Benefits of Cross-Region Inference

1. **Higher Throughput**: Automatically distributes load across regions
2. **Better Availability**: Seamless failover during capacity constraints
3. **Simplified Management**: Single endpoint for multi-region deployment

## Supported Models

See [MODELS.md](./MODELS.md) for a comprehensive list of available models in EU regions.

### Popular Models

#### Claude 3.7 Sonnet (Latest)
- **Model ID**: `bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0`
- **Cross-Region**: `bedrock/eu.anthropic.claude-3-7-sonnet-20250219-v1:0`
- **Best for**: General purpose, coding, complex reasoning

#### Claude 3.5 Sonnet v2
- **Model ID**: `bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0`
- **Best for**: Balanced performance and cost

#### Claude 3 Haiku
- **Model ID**: `bedrock/anthropic.claude-3-haiku-20240307-v1:0`
- **Best for**: Fast, cost-effective tasks

#### Llama 3.1 70B
- **Model ID**: `bedrock/meta.llama-3-1-70b-instruct-v1:0`
- **Best for**: Open-source alternative with strong capabilities

#### Amazon Titan Text Express
- **Model ID**: `bedrock/amazon.titan-text-express-v1`
- **Best for**: AWS-native, cost-effective option

## Authentication

### Option 1: AWS Named Profile (Recommended)

Use a named profile from `~/.aws/credentials`:

```python
cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
cognee.config.aws_profile_name = "my-profile"
cognee.config.aws_region_name = "eu-central-1"
```

**Environment Variable:**
```bash
export AWS_PROFILE_NAME=my-profile
export AWS_REGION_NAME=eu-central-1
```

### Option 2: Explicit Credentials

Provide credentials explicitly via configuration:

```python
cognee.config.aws_access_key_id = "YOUR_KEY"
cognee.config.aws_secret_access_key = "YOUR_SECRET"
cognee.config.aws_region_name = "eu-central-1"
```

### Option 3: Default Credentials Chain

Cognee can use AWS default credentials from:
- Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
- AWS credentials file (`~/.aws/credentials`) - default profile
- IAM role (when running on EC2, ECS, Lambda, etc.)

Just omit the credential configuration:

```python
cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
cognee.config.aws_region_name = "eu-central-1"
# Credentials will be loaded automatically
```

**Priority Order:**
1. AWS Profile Name (if specified)
2. Explicit Access Key/Secret Key
3. Default credentials chain

## IAM Permissions

Your AWS IAM role or user needs the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/*",
        "arn:aws:bedrock:*:*:inference-profile/*"
      ]
    }
  ]
}
```

For cross-region inference, also include:

```json
{
  "Effect": "Allow",
  "Action": [
    "bedrock:ListCrossRegionInferenceProfiles",
    "bedrock:GetInferenceProfile"
  ],
  "Resource": "*"
}
```

## Model Access

Before using AWS Bedrock models, you must enable model access in the AWS Bedrock console:

1. Go to AWS Bedrock console in your chosen region
2. Navigate to "Model access" in the left sidebar
3. Click "Manage model access" or "Enable specific models"
4. Select the models you want to use (e.g., Claude, Llama, Titan)
5. Review and enable access

This is a one-time setup per region. For cross-region inference, enable access in the source region.

## Configuration Options

### litellm_instructor Configuration

| Environment Variable | Python Config | Description | Default |
|---------------------|---------------|-------------|---------|
| `LLM_PROVIDER` | `llm_provider` | Set to `aws_bedrock` | `openai` |
| `LLM_MODEL` | `llm_model` | Model ID with `bedrock/` prefix | - |
| `AWS_REGION_NAME` | `aws_region_name` | AWS region | `eu-central-1` |
| `AWS_ACCESS_KEY_ID` | `aws_access_key_id` | AWS access key | From default chain |
| `AWS_SECRET_ACCESS_KEY` | `aws_secret_access_key` | AWS secret key | From default chain |

### BAML Configuration

| Environment Variable | Python Config | Description | Default |
|---------------------|---------------|-------------|---------|
| `STRUCTURED_OUTPUT_FRAMEWORK` | `structured_output_framework` | Set to `baml` | `instructor` |
| `BAML_LLM_PROVIDER` | `baml_llm_provider` | Set to `aws_bedrock` | `openai` |
| `BAML_LLM_MODEL` | `baml_llm_model` | Model ID without `bedrock/` prefix | - |
| `BAML_LLM_ENDPOINT` | `baml_llm_endpoint` | AWS region (used as endpoint) | - |

## Fallback Configuration

Configure fallback models for content policy violations:

```python
cognee.config.fallback_model = "bedrock/anthropic.claude-3-haiku-20240307-v1:0"
cognee.config.fallback_endpoint = "eu-west-1"  # Fallback region
```

## Examples

### Example 1: Basic Text Generation

```python
import cognee

# Configure AWS Bedrock
cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
cognee.config.aws_region_name = "eu-central-1"

# Use cognee as normal
await cognee.add("Your data here")
await cognee.cognify()
```

### Example 2: Cross-Region Inference

```python
import cognee

# Use cross-region inference profile for EU
cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/eu.anthropic.claude-3-7-sonnet-20250219-v1:0"
cognee.config.aws_region_name = "eu-central-1"

# Requests will be routed across EU regions automatically
await cognee.add("Your data here")
await cognee.cognify()
```

### Example 3: Using BAML with AWS Bedrock

```python
import cognee

# Configure BAML framework with AWS Bedrock
cognee.config.structured_output_framework = "baml"
cognee.config.baml_llm_provider = "aws_bedrock"
cognee.config.baml_llm_model = "anthropic.claude-3-7-sonnet-20250219-v1:0"
cognee.config.baml_llm_endpoint = "eu-west-1"

# Use cognee with BAML
await cognee.add("Your data here")
await cognee.cognify()
```

### Example 4: Using Default AWS Credentials

```python
import cognee

# No explicit credentials - uses default AWS credentials chain
cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
cognee.config.aws_region_name = "eu-central-1"

# Will use credentials from ~/.aws/credentials or IAM role
await cognee.add("Your data here")
await cognee.cognify()
```

## Troubleshooting

### Error: "Model access denied"

**Solution**: Enable model access in AWS Bedrock console for the chosen region.

### Error: "Region not supported"

**Solution**: Verify the model is available in your chosen region. See [MODELS.md](./MODELS.md) for region availability.

### Error: "Invalid credentials"

**Solution**: Check your AWS credentials are correctly configured. Test with AWS CLI:
```bash
aws bedrock list-foundation-models --region eu-central-1
```

### Error: "Rate limit exceeded"

**Solution**: Consider using cross-region inference profiles to distribute load, or implement rate limiting in your application.

## Performance Considerations

1. **Model Selection**: Claude 3 Haiku is faster and cheaper for simple tasks
2. **Cross-Region Inference**: Adds 10-50ms latency but provides better throughput
3. **Region Selection**: Choose regions closest to your users for lower latency
4. **Caching**: Cognee automatically caches results where possible

## Cost Optimization

1. Use smaller models (Haiku, Titan Lite) for simpler tasks
2. Enable cross-region inference for better capacity utilization
3. Monitor usage via AWS Cost Explorer
4. Consider reserved capacity for predictable workloads

## Additional Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [AWS Bedrock Cross-Region Inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)
- [LiteLLM AWS Bedrock Provider](https://docs.litellm.ai/docs/providers/bedrock)
- [BAML Documentation](https://docs.boundaryml.com/)
- [Cognee Documentation](https://docs.cognee.ai/)

## Support

For issues or questions:
- GitHub Issues: [cognee/issues](https://github.com/PhilippMT/cognee/issues)
- Discord: [Join Discord](https://discord.gg/NQPKmU5CCg)
- Documentation: [docs.cognee.ai](https://docs.cognee.ai/)
