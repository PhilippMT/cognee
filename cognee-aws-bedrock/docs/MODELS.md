# AWS Bedrock Foundation Models - Complete Configuration Guide

This document provides comprehensive configuration information for all AWS Bedrock foundation models available in **eu-central-1** and **eu-north-1** regions, with proper setup for instructor[bedrock] including tools/function calling support.

## Table of Contents

- [Quick Reference](#quick-reference)
- [Anthropic Claude Models](#anthropic-claude-models)
- [Amazon Nova Models](#amazon-nova-models)
- [Meta Llama Models](#meta-llama-models)
- [Mistral AI Models](#mistral-ai-models)
- [Amazon Titan Models](#amazon-titan-models)
- [Cohere Models](#cohere-models)
- [Cross-Region Inference Profiles](#cross-region-inference-profiles)
- [Configuration Examples](#configuration-examples)

## Quick Reference

### Models with Tools/Function Calling Support

All models below support **BEDROCK_TOOLS** mode with instructor[bedrock], providing native function calling capabilities:

| Provider | Model Count | Best For |
|----------|-------------|----------|
| Anthropic Claude | 5 models | Complex reasoning, multimodal understanding |
| Amazon Nova | 3 models | Multimodal (text, image, video), cost-effective |
| Meta Llama | 8 models | Open-source, customizable, various sizes |
| Mistral AI | 4 models | European compliance, strong performance |
| Cohere | 2 models | RAG, search, multilingual |

### Models without Tools Support (JSON mode only)

- **Amazon Titan** models (3 models): Use BEDROCK_JSON mode

---

## Anthropic Claude Models

All Claude models support **tools/function calling** with `BEDROCK_TOOLS` mode.

### Claude 3.5 Sonnet v2 (Latest)

**Model ID:** `anthropic.claude-3-5-sonnet-20241022-v2:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 200,000 tokens
- **Max Output:** 8,192 tokens
- **Input Modalities:** Text, Image
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Most complex tasks, latest features, best reasoning

**Configuration:**
```python
import cognee
from cognee_aws_bedrock import register_bedrock_adapters

register_bedrock_adapters(llm_region="eu-central-1")

cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"
cognee.config.aws_region_name = "eu-central-1"
```

### Claude 3.5 Sonnet v1

**Model ID:** `anthropic.claude-3-5-sonnet-20240620-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 200,000 tokens
- **Max Output:** 8,192 tokens
- **Input Modalities:** Text, Image
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Production workloads, balanced cost/performance

### Claude 3.5 Haiku

**Model ID:** `anthropic.claude-3-5-haiku-20241022-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 200,000 tokens
- **Max Output:** 8,192 tokens
- **Input Modalities:** Text, Image
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Fast responses, cost-effective, high volume

### Claude 3 Sonnet

**Model ID:** `anthropic.claude-3-sonnet-20240229-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 200,000 tokens
- **Max Output:** 4,096 tokens
- **Input Modalities:** Text, Image
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Established workloads, reliable performance

### Claude 3 Haiku

**Model ID:** `anthropic.claude-3-haiku-20240307-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 200,000 tokens
- **Max Output:** 4,096 tokens
- **Input Modalities:** Text, Image
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Ultra-fast responses, simple tasks

---

## Amazon Nova Models

Amazon's newest multimodal models with **tools/function calling** support.

### Nova Pro

**Model ID:** `amazon.nova-pro-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 300,000 tokens
- **Max Output:** 5,120 tokens
- **Input Modalities:** Text, Image, Video
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Multimodal understanding, video analysis, complex tasks

**Configuration:**
```python
cognee.config.llm_model = "bedrock/amazon.nova-pro-v1:0"
```

### Nova Lite

**Model ID:** `amazon.nova-lite-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 300,000 tokens
- **Max Output:** 5,120 tokens
- **Input Modalities:** Text, Image, Video
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Cost-effective multimodal, fast processing

### Nova Micro

**Model ID:** `amazon.nova-micro-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 128,000 tokens
- **Max Output:** 5,120 tokens
- **Input Modalities:** Text
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Text-only tasks, extremely cost-effective

---

## Meta Llama Models

Open-source models with **tools/function calling** support.

### Llama 3.3 70B Instruct

**Model ID:** `meta.llama3-3-70b-instruct-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 128,000 tokens
- **Max Output:** 2,048 tokens
- **Input Modalities:** Text
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Latest Llama, strong performance, open-source

### Llama 3.2 90B Vision Instruct

**Model ID:** `meta.llama3-2-90b-instruct-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 128,000 tokens
- **Max Output:** 2,048 tokens
- **Input Modalities:** Text, Image
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Vision tasks, multimodal, largest Llama 3.2

### Llama 3.2 11B Vision Instruct

**Model ID:** `meta.llama3-2-11b-instruct-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 128,000 tokens
- **Max Output:** 2,048 tokens
- **Input Modalities:** Text, Image
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Efficient vision model, cost-effective

### Llama 3.2 3B and 1B Instruct

**Model IDs:**
- `meta.llama3-2-3b-instruct-v1:0` (3B)
- `meta.llama3-2-1b-instruct-v1:0` (1B)

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 128,000 tokens
- **Max Output:** 2,048 tokens
- **Input Modalities:** Text
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Edge deployment, ultra-low latency, high volume

### Llama 3.1 Series

**Model IDs:**
- `meta.llama3-1-405b-instruct-v1:0` (405B - Largest)
- `meta.llama3-1-70b-instruct-v1:0` (70B)
- `meta.llama3-1-8b-instruct-v1:0` (8B)

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 128,000 tokens
- **Max Output:** 2,048 tokens
- **Input Modalities:** Text
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Flexible scaling options, proven performance

**Configuration:**
```python
# Using the largest Llama model
cognee.config.llm_model = "bedrock/meta.llama3-1-405b-instruct-v1:0"

# Or the most efficient
cognee.config.llm_model = "bedrock/meta.llama3-2-1b-instruct-v1:0"
```

---

## Mistral AI Models

European AI company models with **tools/function calling** support.

### Mistral Large 2 (2407)

**Model ID:** `mistral.mistral-large-2407-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 128,000 tokens
- **Max Output:** 8,192 tokens
- **Input Modalities:** Text
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Latest Mistral, best performance, complex reasoning

### Mistral Large (2402)

**Model ID:** `mistral.mistral-large-2402-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 32,000 tokens
- **Max Output:** 8,192 tokens
- **Input Modalities:** Text
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Production workloads, European compliance

### Mistral Small (2402)

**Model ID:** `mistral.mistral-small-2402-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 32,000 tokens
- **Max Output:** 8,192 tokens
- **Input Modalities:** Text
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Cost-effective, fast, good balance

### Mixtral 8x7B Instruct

**Model ID:** `mistral.mixtral-8x7b-instruct-v0:1`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 32,000 tokens
- **Max Output:** 4,096 tokens
- **Input Modalities:** Text
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Mixture of experts, efficient, open weights

**Configuration:**
```python
cognee.config.llm_model = "bedrock/mistral.mistral-large-2407-v1:0"
```

---

## Amazon Titan Models

**Note:** Titan models do NOT support tools/function calling. Use **BEDROCK_JSON** mode.

### Titan Text Premier

**Model ID:** `amazon.titan-text-premier-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 32,000 tokens
- **Max Output:** 3,072 tokens
- **Input Modalities:** Text
- **Tools Support:** ❌ No (use BEDROCK_JSON)
- **Streaming:** ✅ Yes
- **Best For:** RAG, summarization, AWS-native

### Titan Text Express

**Model ID:** `amazon.titan-text-express-v1`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 8,000 tokens
- **Max Output:** 8,192 tokens
- **Input Modalities:** Text
- **Tools Support:** ❌ No (use BEDROCK_JSON)
- **Streaming:** ✅ Yes
- **Best For:** Fast responses, cost-effective

### Titan Text Lite

**Model ID:** `amazon.titan-text-lite-v1`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 4,000 tokens
- **Max Output:** 4,096 tokens
- **Input Modalities:** Text
- **Tools Support:** ❌ No (use BEDROCK_JSON)
- **Streaming:** ✅ Yes
- **Best For:** Simple tasks, lowest cost

**Configuration:**
```python
# Titan models automatically use BEDROCK_JSON mode
cognee.config.llm_model = "bedrock/amazon.titan-text-premier-v1:0"
```

---

## Cohere Models

Command R series with **tools/function calling** support.

### Command R+

**Model ID:** `cohere.command-r-plus-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 128,000 tokens
- **Max Output:** 4,096 tokens
- **Input Modalities:** Text
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** RAG, search, retrieval, complex reasoning

### Command R

**Model ID:** `cohere.command-r-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 128,000 tokens
- **Max Output:** 4,096 tokens
- **Input Modalities:** Text
- **Tools Support:** ✅ Yes (BEDROCK_TOOLS)
- **Streaming:** ✅ Yes
- **Best For:** Cost-effective RAG, search optimization

**Configuration:**
```python
cognee.config.llm_model = "bedrock/cohere.command-r-plus-v1:0"
```

---

## Cross-Region Inference Profiles

For automatic load distribution across EU regions, use cross-region inference profiles with the `eu.` prefix:

```python
# Claude with cross-region inference
cognee.config.llm_model = "bedrock/eu.anthropic.claude-3-5-sonnet-20241022-v2:0"

# Amazon Nova with cross-region inference
cognee.config.llm_model = "bedrock/eu.amazon.nova-pro-v1:0"

# Cohere with cross-region inference
cognee.config.llm_model = "bedrock/eu.cohere.command-r-plus-v1:0"
```

**Available Cross-Region Profiles:**

**Anthropic Claude:**
- `eu.anthropic.claude-3-5-sonnet-20241022-v2:0`
- `eu.anthropic.claude-3-5-sonnet-20240620-v1:0`
- `eu.anthropic.claude-3-5-haiku-20241022-v1:0`
- `eu.anthropic.claude-3-sonnet-20240229-v1:0`
- `eu.anthropic.claude-3-haiku-20240307-v1:0`

**Amazon Nova:**
- `eu.amazon.nova-pro-v1:0`
- `eu.amazon.nova-lite-v1:0`
- `eu.amazon.nova-micro-v1:0`

**Cohere:**
- `eu.cohere.command-r-plus-v1:0`
- `eu.cohere.command-r-v1:0`

---

## Configuration Examples

### Basic Configuration

```python
from cognee_aws_bedrock import register_bedrock_adapters
import cognee

# Register adapters
register_bedrock_adapters(llm_region="eu-central-1")

# Configure LLM
cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"
cognee.config.aws_region_name = "eu-central-1"

# Use Cognee
await cognee.add("Your data here")
await cognee.cognify()
```

### With AWS Profile

```python
register_bedrock_adapters(
    llm_region="eu-central-1",
    llm_profile="my-aws-profile"
)

cognee.config.llm_model = "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"
cognee.config.aws_profile_name = "my-aws-profile"
```

### Multi-Region Setup

```python
# Use different regions for different purposes
register_bedrock_adapters(
    llm_region="eu-central-1",      # Primary region
    embedding_region="eu-north-1"    # Embedding region
)

cognee.config.llm_model = "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"
cognee.config.aws_region_name = "eu-central-1"
```

### With Fallback Model

```python
from cognee_aws_bedrock.llm import BedrockLLMAdapter

adapter = BedrockLLMAdapter(
    model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    max_completion_tokens=4096,
    aws_region_name="eu-central-1",
    fallback_model="anthropic.claude-3-5-haiku-20241022-v1:0",
    fallback_aws_region_name="eu-north-1"
)
```

### Using Environment Variables

```bash
# Set environment variables
export LLM_PROVIDER=aws_bedrock
export LLM_MODEL=bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0
export AWS_REGION_NAME=eu-central-1
export AWS_PROFILE_NAME=my-profile
```

```python
# Then simply use
import cognee
from cognee_aws_bedrock import register_bedrock_adapters

register_bedrock_adapters()
# Configuration is read from environment variables
```

---

## Model Selection Guide

### By Use Case

**Complex Reasoning & Analysis:**
- Claude 3.5 Sonnet v2
- Mistral Large 2
- Llama 3.1 405B

**Multimodal (Text + Image/Video):**
- Amazon Nova Pro
- Claude 3.5 Sonnet/Haiku
- Llama 3.2 90B/11B Vision

**Cost-Effective Production:**
- Amazon Nova Micro/Lite
- Claude 3.5 Haiku
- Llama 3.2 3B/1B
- Mistral Small

**RAG & Search:**
- Cohere Command R+
- Cohere Command R
- Amazon Titan Premier

**Open Source / Customizable:**
- Meta Llama 3.x series (all sizes)
- Mistral Mixtral 8x7B

### By Budget

**Premium (Best Performance):**
- Claude 3.5 Sonnet v2
- Amazon Nova Pro
- Llama 3.1 405B

**Balanced (Good Performance/Cost):**
- Claude 3.5 Haiku
- Mistral Large/Small
- Amazon Nova Lite
- Llama 3.1 70B

**Economy (Cost-Optimized):**
- Amazon Nova Micro
- Llama 3.2 3B/1B
- Amazon Titan Express/Lite

---

## Tools/Function Calling Support

### Models with Native Tools Support (BEDROCK_TOOLS mode)

All models support structured outputs through instructor[bedrock], but the following have **native tools/function calling**:

✅ **All Anthropic Claude models**
✅ **All Amazon Nova models**
✅ **All Meta Llama models**
✅ **All Mistral AI models**
✅ **All Cohere Command R models**

### Models with JSON Mode Only

❌ Amazon Titan models (use BEDROCK_JSON mode)

### Example with Tools

```python
from pydantic import BaseModel
from typing import List

class Entity(BaseModel):
    name: str
    type: str
    confidence: float

class Extraction(BaseModel):
    entities: List[Entity]
    summary: str

# With tools support (Claude, Nova, Llama, Mistral, Cohere)
cognee.config.llm_model = "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"

# The adapter automatically uses BEDROCK_TOOLS mode
# Provides structured outputs with full validation
```

---

## Performance Considerations

### Latency

**Lowest Latency:**
- Llama 3.2 1B/3B
- Amazon Nova Micro
- Claude 3.5 Haiku

**Balanced:**
- Llama 3.1 8B/70B
- Mistral Small
- Amazon Nova Lite

**Higher Latency (Complex Tasks):**
- Claude 3.5 Sonnet v2
- Llama 3.1 405B
- Amazon Nova Pro

### Token Limits

**Largest Context Windows:**
- Amazon Nova (300K tokens)
- Claude 3.x (200K tokens)
- Meta Llama 3.x (128K tokens)
- Cohere Command R (128K tokens)
- Mistral Large 2 (128K tokens)

**Smaller Context:**
- Mistral Large 2402/Small (32K)
- Amazon Titan (4K-32K)

---

## Best Practices

1. **Start with Claude 3.5 Sonnet v2** for best overall performance
2. **Use cross-region profiles** (`eu.*`) for automatic load distribution
3. **Match model to task**: Don't use 405B for simple tasks
4. **Consider cost**: Haiku/Nova Micro for high-volume simple tasks
5. **Test multiple models**: Use different models for different components
6. **Monitor usage**: Set up CloudWatch alarms for cost tracking
7. **Use fallback models**: Configure fallback for content policy issues

---

## Getting Help

- **Documentation**: [docs.cognee.ai](https://docs.cognee.ai)
- **AWS Bedrock Docs**: [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- **Instructor Docs**: [python.useinstructor.com](https://python.useinstructor.com)
- **GitHub Issues**: [cognee/issues](https://github.com/topoteretes/cognee/issues)
