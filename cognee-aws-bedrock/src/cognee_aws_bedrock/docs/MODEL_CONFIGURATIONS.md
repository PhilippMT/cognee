# Complete AWS Bedrock Model Configurations for EU Regions

This document provides configuration examples for **EVERY SINGLE** AWS Bedrock foundation model available in European regions (eu-central-1, eu-west-1, eu-north-1, eu-west-2, eu-west-3).

## Table of Contents

- [LLM Models](#llm-models)
  - [Anthropic Claude](#anthropic-claude)
  - [Meta Llama](#meta-llama)
  - [Amazon Titan Text](#amazon-titan-text)
  - [Amazon Nova](#amazon-nova)
  - [Mistral AI](#mistral-ai)
  - [Cohere Command](#cohere-command)
- [Embedding Models](#embedding-models)
  - [Amazon Titan Embeddings](#amazon-titan-embeddings)
  - [Cohere Embeddings](#cohere-embeddings)
- [Cross-Region Inference Profiles](#cross-region-inference-profiles)
- [Batch Processing](#batch-processing)

---

## LLM Models

### Anthropic Claude

#### Claude 3.7 Sonnet (Latest - February 2025)

**Model ID**: `anthropic.claude-3-7-sonnet-20250219-v1:0`  
**Regions**: eu-central-1, eu-north-1, eu-west-1, eu-west-2, eu-west-3  
**Cross-Region**: `eu.anthropic.claude-3-7-sonnet-20250219-v1:0`  
**Context Window**: 200K tokens  
**Max Output**: 8K tokens

```python
from cognee_aws_bedrock import register_bedrock_adapters
import cognee

register_bedrock_adapters(llm_region="eu-central-1")
cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
```

**Environment Variables:**
```bash
LLM_PROVIDER=aws_bedrock
LLM_MODEL=bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0
AWS_REGION_NAME=eu-central-1
AWS_PROFILE_NAME=my-profile  # Optional
```

---

#### Claude 3.5 Sonnet v2 (October 2024)

**Model ID**: `anthropic.claude-3-5-sonnet-20241022-v2:0`  
**Regions**: eu-central-1, eu-west-1  
**Context Window**: 200K tokens  
**Max Output**: 8K tokens

```python
register_bedrock_adapters(llm_region="eu-west-1")
cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"
```

**Environment Variables:**
```bash
LLM_MODEL=bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0
AWS_REGION_NAME=eu-west-1
```

---

#### Claude 3.5 Sonnet v1 (June 2024)

**Model ID**: `anthropic.claude-3-5-sonnet-20240620-v1:0`  
**Regions**: eu-central-1, eu-west-1, eu-west-2, eu-west-3  
**Context Window**: 200K tokens  
**Max Output**: 4K tokens

```python
cognee.config.llm_model = "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0"
```

---

#### Claude 3 Sonnet

**Model ID**: `anthropic.claude-3-sonnet-20240229-v1:0`  
**Regions**: eu-central-1, eu-west-1, eu-west-2, eu-west-3  
**Context Window**: 200K tokens  
**Max Output**: 4K tokens

```python
cognee.config.llm_model = "bedrock/anthropic.claude-3-sonnet-20240229-v1:0"
```

---

#### Claude 3 Haiku

**Model ID**: `anthropic.claude-3-haiku-20240307-v1:0`  
**Regions**: eu-central-1, eu-west-1, eu-west-2, eu-west-3  
**Context Window**: 200K tokens  
**Max Output**: 4K tokens  
**Best for**: Fast, cost-effective tasks

```python
cognee.config.llm_model = "bedrock/anthropic.claude-3-haiku-20240307-v1:0"
```

---

### Meta Llama

#### Llama 3.2 1B Instruct

**Model ID**: `meta.llama-3-2-1b-instruct-v1:0`  
**Regions**: Check AWS console for EU availability  
**Context Window**: 128K tokens  
**Parameters**: 1 Billion

```python
cognee.config.llm_model = "bedrock/meta.llama-3-2-1b-instruct-v1:0"
```

---

#### Llama 3.2 3B Instruct

**Model ID**: `meta.llama-3-2-3b-instruct-v1:0`  
**Regions**: Check AWS console for EU availability  
**Context Window**: 128K tokens  
**Parameters**: 3 Billion

```python
cognee.config.llm_model = "bedrock/meta.llama-3-2-3b-instruct-v1:0"
```

---

#### Llama 3.2 11B Vision Instruct

**Model ID**: `meta.llama-3-2-11b-instruct-v1:0`  
**Regions**: Check AWS console for EU availability  
**Context Window**: 128K tokens  
**Parameters**: 11 Billion  
**Capabilities**: Text + Image input

```python
cognee.config.llm_model = "bedrock/meta.llama-3-2-11b-instruct-v1:0"
```

---

#### Llama 3.2 90B Vision Instruct

**Model ID**: `meta.llama-3-2-90b-instruct-v1:0`  
**Regions**: Check AWS console for EU availability  
**Context Window**: 128K tokens  
**Parameters**: 90 Billion  
**Capabilities**: Text + Image input

```python
cognee.config.llm_model = "bedrock/meta.llama-3-2-90b-instruct-v1:0"
```

---

#### Llama 3.1 8B Instruct

**Model ID**: `meta.llama-3-1-8b-instruct-v1:0`  
**Regions**: eu-central-1, eu-west-1, eu-west-2, eu-west-3  
**Context Window**: 128K tokens  
**Parameters**: 8 Billion

```python
cognee.config.llm_model = "bedrock/meta.llama-3-1-8b-instruct-v1:0"
```

---

#### Llama 3.1 70B Instruct

**Model ID**: `meta.llama-3-1-70b-instruct-v1:0`  
**Regions**: eu-central-1, eu-west-1, eu-west-2, eu-west-3  
**Context Window**: 128K tokens  
**Parameters**: 70 Billion

```python
cognee.config.llm_model = "bedrock/meta.llama-3-1-70b-instruct-v1:0"
```

---

#### Llama 3.1 405B Instruct

**Model ID**: `meta.llama-3-1-405b-instruct-v1:0`  
**Regions**: eu-west-1, eu-west-2 (limited availability)  
**Context Window**: 128K tokens  
**Parameters**: 405 Billion  
**Best for**: Most complex reasoning tasks

```python
cognee.config.llm_model = "bedrock/meta.llama-3-1-405b-instruct-v1:0"
cognee.config.aws_region_name = "eu-west-1"
```

---

### Amazon Titan Text

#### Titan Text Premier

**Model ID**: `amazon.titan-text-premier-v1:0`  
**Regions**: eu-central-1, eu-west-1  
**Context Window**: 32K tokens  
**Max Output**: 3K tokens

```python
cognee.config.llm_model = "bedrock/amazon.titan-text-premier-v1:0"
```

---

#### Titan Text Express

**Model ID**: `amazon.titan-text-express-v1`  
**Regions**: eu-central-1, eu-west-1, eu-west-2, eu-west-3  
**Context Window**: 8K tokens  
**Max Output**: 8K tokens

```python
cognee.config.llm_model = "bedrock/amazon.titan-text-express-v1"
```

---

#### Titan Text Lite

**Model ID**: `amazon.titan-text-lite-v1`  
**Regions**: eu-central-1, eu-west-1, eu-west-2, eu-west-3  
**Context Window**: 4K tokens  
**Max Output**: 4K tokens  
**Best for**: Cost-effective simple tasks

```python
cognee.config.llm_model = "bedrock/amazon.titan-text-lite-v1"
```

---

### Amazon Nova

#### Nova Micro

**Model ID**: `amazon.nova-micro-v1:0`  
**Regions**: eu-central-1, eu-west-1  
**Context Window**: 128K tokens  
**Best for**: Ultra-fast, lightweight tasks

```python
cognee.config.llm_model = "bedrock/amazon.nova-micro-v1:0"
```

---

#### Nova Lite

**Model ID**: `amazon.nova-lite-v1:0`  
**Regions**: eu-central-1, eu-west-1  
**Context Window**: 300K tokens

```python
cognee.config.llm_model = "bedrock/amazon.nova-lite-v1:0"
```

---

#### Nova Pro

**Model ID**: `amazon.nova-pro-v1:0`  
**Regions**: eu-central-1, eu-west-1  
**Context Window**: 300K tokens  
**Capabilities**: Text, Image, Video input

```python
cognee.config.llm_model = "bedrock/amazon.nova-pro-v1:0"
```

---

### Mistral AI

#### Mistral 7B Instruct

**Model ID**: `mistral.mistral-7b-instruct-v0:2`  
**Regions**: eu-central-1, eu-west-1, eu-west-3  
**Context Window**: 32K tokens  
**Parameters**: 7 Billion

```python
cognee.config.llm_model = "bedrock/mistral.mistral-7b-instruct-v0:2"
```

---

#### Mixtral 8x7B Instruct

**Model ID**: `mistral.mixtral-8x7b-instruct-v0:1`  
**Regions**: eu-central-1, eu-west-1, eu-west-3  
**Context Window**: 32K tokens  
**Parameters**: 56 Billion (8x7B MoE)

```python
cognee.config.llm_model = "bedrock/mistral.mixtral-8x7b-instruct-v0:1"
```

---

#### Mistral Large

**Model ID**: `mistral.mistral-large-2402-v1:0`  
**Regions**: eu-central-1, eu-west-1, eu-west-3  
**Context Window**: 32K tokens

```python
cognee.config.llm_model = "bedrock/mistral.mistral-large-2402-v1:0"
```

---

### Cohere Command

#### Command Text

**Model ID**: `cohere.command-text-v14`  
**Regions**: eu-central-1, eu-west-1, eu-west-3  
**Context Window**: 4K tokens

```python
cognee.config.llm_model = "bedrock/cohere.command-text-v14"
```

---

#### Command Light Text

**Model ID**: `cohere.command-light-text-v14`  
**Regions**: eu-central-1, eu-west-1, eu-west-3  
**Context Window**: 4K tokens

```python
cognee.config.llm_model = "bedrock/cohere.command-light-text-v14"
```

---

#### Command R

**Model ID**: `cohere.command-r-v1:0`  
**Regions**: eu-central-1, eu-west-1, eu-west-3  
**Context Window**: 128K tokens

```python
cognee.config.llm_model = "bedrock/cohere.command-r-v1:0"
```

---

#### Command R+

**Model ID**: `cohere.command-r-plus-v1:0`  
**Regions**: eu-central-1, eu-west-1, eu-west-3  
**Context Window**: 128K tokens  
**Best for**: Complex reasoning with large context

```python
cognee.config.llm_model = "bedrock/cohere.command-r-plus-v1:0"
```

---

## Embedding Models

### Amazon Titan Embeddings

#### Titan Embed Text V2

**Model ID**: `amazon.titan-embed-text-v2:0`  
**Regions**: eu-central-1, eu-west-1, eu-west-3  
**Dimensions**: 256, 512, or 1024 (configurable)  
**Max Input**: 8,192 tokens / 50,000 characters  
**Languages**: English + 100+ multilingual

```python
from cognee_aws_bedrock import register_bedrock_adapters
import cognee

register_bedrock_adapters(embedding_region="eu-central-1")
cognee.config.embedding_provider = "bedrock"
cognee.config.embedding_model = "bedrock/amazon.titan-embed-text-v2:0"
cognee.config.embedding_dimensions = 1024
```

**Environment Variables:**
```bash
EMBEDDING_PROVIDER=bedrock
EMBEDDING_MODEL=bedrock/amazon.titan-embed-text-v2:0
EMBEDDING_DIMENSIONS=1024
AWS_REGION_NAME=eu-central-1
```

**With different dimensions:**
```python
# 256 dimensions (faster, less accurate)
cognee.config.embedding_dimensions = 256

# 512 dimensions (balanced)
cognee.config.embedding_dimensions = 512

# 1024 dimensions (slower, more accurate)
cognee.config.embedding_dimensions = 1024
```

---

#### Titan Embed Text V1

**Model ID**: `amazon.titan-embed-text-v1`  
**Regions**: eu-central-1, eu-west-1, eu-west-2, eu-west-3  
**Dimensions**: 1536  
**Max Input**: 8,192 tokens  
**Languages**: English optimized

```python
cognee.config.embedding_provider = "bedrock"
cognee.config.embedding_model = "bedrock/amazon.titan-embed-text-v1"
cognee.config.embedding_dimensions = 1536
```

---

#### Titan Embed Image V1 (Multimodal)

**Model ID**: `amazon.titan-embed-image-v1`  
**Regions**: Limited EU availability (check console)  
**Dimensions**: 1024  
**Capabilities**: Text and Image embeddings

```python
cognee.config.embedding_model = "bedrock/amazon.titan-embed-image-v1"
cognee.config.embedding_dimensions = 1024
```

---

### Cohere Embeddings

#### Cohere Embed English V3

**Model ID**: `cohere.embed-english-v3`  
**Regions**: eu-central-1, eu-west-1, eu-west-3  
**Dimensions**: 1024  
**Languages**: English optimized  
**Use Cases**: Search, classification, clustering

```python
cognee.config.embedding_provider = "bedrock"
cognee.config.embedding_model = "bedrock/cohere.embed-english-v3"
cognee.config.embedding_dimensions = 1024
```

---

#### Cohere Embed Multilingual V3

**Model ID**: `cohere.embed-multilingual-v3`  
**Regions**: eu-central-1, eu-west-1, eu-west-3  
**Dimensions**: 1024  
**Languages**: 100+ languages

```python
cognee.config.embedding_model = "bedrock/cohere.embed-multilingual-v3"
cognee.config.embedding_dimensions = 1024
```

---

## Cross-Region Inference Profiles

### EU Cross-Region Profiles

#### Claude 3.7 Sonnet - EU

**Profile ID**: `eu.anthropic.claude-3-7-sonnet-20250219-v1:0`  
**Destination Regions**: eu-central-1, eu-north-1, eu-west-1, eu-west-2, eu-west-3

```python
register_bedrock_adapters(llm_region="eu-central-1")
cognee.config.llm_model = "bedrock/eu.anthropic.claude-3-7-sonnet-20250219-v1:0"
```

---

#### Claude 3.5 Sonnet - EU

**Profile ID**: `eu.anthropic.claude-3-5-sonnet-20241022-v2:0`

```python
cognee.config.llm_model = "bedrock/eu.anthropic.claude-3-5-sonnet-20241022-v2:0"
```

---

#### Cohere Embed V4 - EU

**Profile ID**: `eu.cohere.embed-multilingual-v4:0`  
**Dimensions**: 1024

```python
cognee.config.embedding_model = "bedrock/eu.cohere.embed-multilingual-v4:0"
```

---

## Batch Processing

### LLM Batch Inference

AWS Bedrock supports batch inference for Anthropic Claude models, allowing cost-effective processing of large datasets.

**Supported Models for Batch:**
- All Claude 3.x models
- Claude 3.5 Sonnet
- Claude 3.7 Sonnet

**Configuration:**
```python
# Batch inference requires using the AWS Bedrock Batch API directly
import boto3

bedrock = boto3.client('bedrock', region_name='eu-central-1')

# Create batch job
response = bedrock.create_model_invocation_job(
    jobName='my-batch-job',
    modelId='anthropic.claude-3-7-sonnet-20250219-v1:0',
    inputDataConfig={
        's3InputDataConfig': {
            's3Uri': 's3://my-bucket/input.jsonl'
        }
    },
    outputDataConfig={
        's3OutputDataConfig': {
            's3Uri': 's3://my-bucket/output/'
        }
    },
    roleArn='arn:aws:iam::ACCOUNT:role/BedrockBatchRole'
)
```

**Batch Input Format (JSONL):**
```json
{"recordId": "1", "modelInput": {"messages": [{"role": "user", "content": "Hello"}]}}
{"recordId": "2", "modelInput": {"messages": [{"role": "user", "content": "Hi there"}]}}
```

---

### Embedding Batch Processing

Embedding models automatically handle batching internally:

**Amazon Titan Embed v2:**
- Batch size: Up to 8,192 tokens per request
- Automatic chunking for larger texts

**Cohere Embed:**
- Batch size: Multiple texts per request
- Handled automatically by litellm

**Optimizing Batch Performance:**
```python
# Process multiple texts efficiently
texts = ["Text 1", "Text 2", ..., "Text N"]

# The adapter automatically batches these
embeddings = await bedrock_embedding_adapter.embed_text(texts)
```

---

## Complete Configuration Example

### Separate Configs for LLM and Embedding

```python
from cognee_aws_bedrock import register_bedrock_adapters
import cognee

# Register with different regions and profiles
register_bedrock_adapters(
    llm_region="eu-west-1",
    llm_profile="production-llm",
    embedding_region="eu-central-1",
    embedding_profile="production-embedding"
)

# Configure LLM - Claude 3.7 Sonnet with cross-region
cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/eu.anthropic.claude-3-7-sonnet-20250219-v1:0"

# Configure Embeddings - Titan v2
cognee.config.embedding_provider = "bedrock"
cognee.config.embedding_model = "bedrock/amazon.titan-embed-text-v2:0"
cognee.config.embedding_dimensions = 1024

# Use Cognee
await cognee.add("Your data")
await cognee.cognify()
```

---

## Environment-Based Configuration

```bash
# LLM Configuration
export LLM_PROVIDER=aws_bedrock
export LLM_MODEL=bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0
export AWS_REGION_NAME=eu-west-1
export AWS_PROFILE_NAME=production-llm

# Embedding Configuration
export EMBEDDING_PROVIDER=bedrock
export EMBEDDING_MODEL=bedrock/amazon.titan-embed-text-v2:0
export EMBEDDING_DIMENSIONS=1024
# Note: Separate region/profile for embeddings requires code-level configuration
```

---

## Regional Availability Summary

### eu-central-1 (Frankfurt)
- ✅ All Claude models
- ✅ Llama 3.1 (8B, 70B)
- ✅ Titan Text & Embeddings
- ✅ Nova models
- ✅ Mistral models
- ✅ Cohere models

### eu-west-1 (Ireland)
- ✅ All Claude models
- ✅ Llama 3.1 (8B, 70B, 405B)
- ✅ Titan Text & Embeddings
- ✅ Nova models
- ✅ Mistral models
- ✅ Cohere models

### eu-north-1 (Stockholm)
- ✅ Claude 3.7 Sonnet
- ⚠️ Limited other models (check console)

### eu-west-2 (London)
- ✅ Most Claude models
- ✅ Llama 3.1 models
- ✅ Titan Text
- ⚠️ Check console for full list

### eu-west-3 (Paris)
- ✅ Most Claude models
- ✅ Llama 3.1 models
- ✅ Titan Text
- ⚠️ Check console for full list

---

## Notes

1. **Model Availability**: Always check the AWS Bedrock console for the latest model availability in your region.
2. **Cross-Region Profiles**: Provide higher throughput and availability by routing across multiple regions.
3. **Batch Processing**: Batch inference is cost-effective for large-scale processing but requires separate API calls.
4. **Profile Configuration**: Use separate AWS profiles for LLM vs embedding for better security and cost tracking.
5. **Dimensions**: Titan Embed v2 supports configurable dimensions (256, 512, 1024) for performance tuning.

---

Last Updated: January 2025
