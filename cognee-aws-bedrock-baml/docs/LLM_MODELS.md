# LLM Models Catalog

Complete catalog of LLM models available in AWS Bedrock EU regions.

## Anthropic Claude Models

All Claude models support tools/function calling.

### Claude 3.5 Sonnet v2 (Latest & Recommended)

| Property | Value |
|----------|-------|
| **Model ID** | `anthropic.claude-3-5-sonnet-20241022-v2:0` |
| **Regions** | eu-central-1, eu-west-1, eu-north-1 |
| **Context Window** | 200,000 tokens |
| **Max Output** | 8,192 tokens |
| **Input Modalities** | Text, Image |
| **Tools Support** | ✅ Yes |
| **Best For** | Complex reasoning, latest features |

### Claude 3.5 Sonnet v1

| Property | Value |
|----------|-------|
| **Model ID** | `anthropic.claude-3-5-sonnet-20240620-v1:0` |
| **Context Window** | 200,000 tokens |
| **Max Output** | 8,192 tokens |

### Claude 3.5 Haiku

| Property | Value |
|----------|-------|
| **Model ID** | `anthropic.claude-3-5-haiku-20241022-v1:0` |
| **Context Window** | 200,000 tokens |
| **Max Output** | 8,192 tokens |
| **Best For** | Fast responses, cost-effective |

### Claude 3 Sonnet

| Property | Value |
|----------|-------|
| **Model ID** | `anthropic.claude-3-sonnet-20240229-v1:0` |
| **Context Window** | 200,000 tokens |
| **Max Output** | 4,096 tokens |

### Claude 3 Haiku

| Property | Value |
|----------|-------|
| **Model ID** | `anthropic.claude-3-haiku-20240307-v1:0` |
| **Context Window** | 200,000 tokens |
| **Max Output** | 4,096 tokens |

---

## Amazon Nova Models

Multimodal models with tools support.

### Nova Pro

| Property | Value |
|----------|-------|
| **Model ID** | `amazon.nova-pro-v1:0` |
| **Regions** | eu-central-1, eu-west-1, eu-north-1 |
| **Context Window** | 300,000 tokens |
| **Max Output** | 5,120 tokens |
| **Input Modalities** | Text, Image, Video |
| **Tools Support** | ✅ Yes |
| **Best For** | Multimodal tasks, video analysis |

### Nova Lite

| Property | Value |
|----------|-------|
| **Model ID** | `amazon.nova-lite-v1:0` |
| **Context Window** | 300,000 tokens |
| **Input Modalities** | Text, Image, Video |
| **Best For** | Cost-effective multimodal |

### Nova Micro

| Property | Value |
|----------|-------|
| **Model ID** | `amazon.nova-micro-v1:0` |
| **Context Window** | 128,000 tokens |
| **Input Modalities** | Text only |
| **Best For** | Extremely cost-effective |

---

## Meta Llama Models

Open-source models with tools support.

### Llama 3.3 70B Instruct (Latest)

| Property | Value |
|----------|-------|
| **Model ID** | `meta.llama3-3-70b-instruct-v1:0` |
| **Regions** | eu-central-1, eu-west-1, eu-north-1 |
| **Context Window** | 128,000 tokens |
| **Max Output** | 2,048 tokens |
| **Tools Support** | ✅ Yes |
| **Best For** | Latest Llama, strong performance |

### Llama 3.2 Vision Models

| Model ID | Size | Vision |
|----------|------|--------|
| `meta.llama3-2-90b-instruct-v1:0` | 90B | ✅ Yes |
| `meta.llama3-2-11b-instruct-v1:0` | 11B | ✅ Yes |

### Llama 3.2 Text Models

| Model ID | Size |
|----------|------|
| `meta.llama3-2-3b-instruct-v1:0` | 3B |
| `meta.llama3-2-1b-instruct-v1:0` | 1B |

### Llama 3.1 Models

| Model ID | Size | Context |
|----------|------|---------|
| `meta.llama3-1-405b-instruct-v1:0` | 405B | 128K |
| `meta.llama3-1-70b-instruct-v1:0` | 70B | 128K |
| `meta.llama3-1-8b-instruct-v1:0` | 8B | 128K |

---

## Mistral AI Models

European AI company, all support tools.

### Mistral Large 2 (2407)

| Property | Value |
|----------|-------|
| **Model ID** | `mistral.mistral-large-2407-v1:0` |
| **Regions** | eu-central-1, eu-west-1, eu-north-1 |
| **Context Window** | 128,000 tokens |
| **Max Output** | 8,192 tokens |
| **Tools Support** | ✅ Yes |
| **Best For** | Best Mistral, complex reasoning |

### Other Mistral Models

| Model ID | Context |
|----------|---------|
| `mistral.mistral-large-2402-v1:0` | 32K |
| `mistral.mistral-small-2402-v1:0` | 32K |
| `mistral.mixtral-8x7b-instruct-v0:1` | 32K |

---

## Cohere Models

Command R series with tools support.

### Command R+

| Property | Value |
|----------|-------|
| **Model ID** | `cohere.command-r-plus-v1:0` |
| **Regions** | eu-central-1, eu-west-1, eu-north-1 |
| **Context Window** | 128,000 tokens |
| **Max Output** | 4,096 tokens |
| **Tools Support** | ✅ Yes |
| **Best For** | RAG, search, retrieval |

### Command R

| Property | Value |
|----------|-------|
| **Model ID** | `cohere.command-r-v1:0` |
| **Context Window** | 128,000 tokens |
| **Max Output** | 4,096 tokens |

---

## AI21 Labs Models

### Jamba 1.5 Large

| Property | Value |
|----------|-------|
| **Model ID** | `ai21.jamba-1-5-large-v1:0` |
| **Regions** | eu-central-1, eu-west-1 |
| **Context Window** | 256,000 tokens |
| **Max Output** | 4,096 tokens |
| **Tools Support** | ✅ Yes |
| **Best For** | Very long context, complex documents |

### Jamba 1.5 Mini

| Property | Value |
|----------|-------|
| **Model ID** | `ai21.jamba-1-5-mini-v1:0` |
| **Context Window** | 256,000 tokens |
| **Max Output** | 4,096 tokens |
| **Best For** | Long context, cost-effective |

### Jurassic-2 Models (No Tools)

| Model ID | Max Output |
|----------|------------|
| `ai21.j2-ultra-v1` | 8,191 tokens |
| `ai21.j2-mid-v1` | 8,191 tokens |

**Note:** Jurassic-2 models do NOT support tools. Use JSON mode.

---

## Amazon Titan Text Models

**Note:** Titan Text models do NOT support tools. Use JSON mode.

| Model ID | Context | Max Output |
|----------|---------|------------|
| `amazon.titan-text-premier-v1:0` | 32K | 3,072 |
| `amazon.titan-text-express-v1` | 8K | 8,192 |
| `amazon.titan-text-lite-v1` | 4K | 4,096 |
