# Embedding Models Catalog

Complete catalog of embedding models available in AWS Bedrock EU regions.

## Amazon Titan Embeddings

### Titan Text Embeddings V2 (Recommended)

| Property | Value |
|----------|-------|
| **Model ID** | `amazon.titan-embed-text-v2:0` |
| **Regions** | eu-central-1, eu-west-1, eu-north-1 |
| **Dimensions** | 256, 512, 1024 (default: 1024) |
| **Max Input Tokens** | 8,192 |
| **Languages** | 100+ (optimized for English) |
| **Use Cases** | RAG, document search, semantic similarity |

**Usage:**
```python
cognee.config.embedding_model = "bedrock/amazon.titan-embed-text-v2:0"
cognee.config.embedding_dimensions = 1024
```

### Titan Text Embeddings V1

| Property | Value |
|----------|-------|
| **Model ID** | `amazon.titan-embed-text-v1` |
| **Regions** | eu-central-1, eu-west-1, eu-north-1 |
| **Dimensions** | 1536 (fixed) |
| **Max Input Tokens** | 8,192 |
| **Languages** | English |

### Titan Multimodal Embeddings G1

| Property | Value |
|----------|-------|
| **Model ID** | `amazon.titan-embed-image-v1` |
| **Regions** | eu-central-1, eu-west-1, eu-north-1 |
| **Dimensions** | 256, 384, 1024 (default: 1024) |
| **Max Input Tokens** | 256 |
| **Input Modalities** | Text, Image (up to 25MB) |
| **Languages** | English |
| **Use Cases** | Image search, multimodal retrieval |

---

## Cohere Embeddings

### Cohere Embed English v3

| Property | Value |
|----------|-------|
| **Model ID** | `cohere.embed-english-v3` |
| **Regions** | eu-central-1, eu-west-1, eu-north-1 |
| **Dimensions** | 1024 |
| **Max Input Tokens** | 512 |
| **Languages** | English |
| **Use Cases** | English text embedding, search |

### Cohere Embed Multilingual v3

| Property | Value |
|----------|-------|
| **Model ID** | `cohere.embed-multilingual-v3` |
| **Regions** | eu-central-1, eu-west-1, eu-north-1 |
| **Dimensions** | 1024 |
| **Max Input Tokens** | 512 |
| **Languages** | 100+ languages |
| **Use Cases** | Multilingual search, cross-language retrieval |

---

## Embedding Model Selection Guide

| Use Case | Recommended Model |
|----------|-------------------|
| **General purpose (English)** | Titan Text Embeddings V2 |
| **Multilingual** | Cohere Embed Multilingual v3 |
| **Image + Text** | Titan Multimodal G1 |
| **High performance** | Cohere Embed English v3 |
| **Long documents** | Titan Text Embeddings V2 (8K tokens) |

## Dimension Selection

| Dimension | Trade-off |
|-----------|-----------|
| 256 | Fastest, lowest storage, lower accuracy |
| 512 | Balanced |
| 1024 | Best accuracy, higher storage |
| 1536 | Titan V1 only, highest resolution |

## Configuration Example

```python
from cognee_aws_bedrock_baml import BamlBedrockEmbeddingAdapter

# Default configuration (recommended)
adapter = BamlBedrockEmbeddingAdapter(
    model="amazon.titan-embed-text-v2:0",
    dimensions=1024,
    aws_region_name="eu-central-1"
)

# Multilingual configuration
adapter = BamlBedrockEmbeddingAdapter(
    model="cohere.embed-multilingual-v3",
    dimensions=1024,
    aws_region_name="eu-west-1"
)
```

## Python Helper Functions

```python
from cognee_aws_bedrock_baml.bedrock_models_config import (
    get_embedding_model_config,
    get_embedding_models_by_region,
    get_all_embedding_models
)

# Get config for specific model
config = get_embedding_model_config("amazon.titan-embed-text-v2:0")
print(f"Dimensions: {config.dimensions}")

# Get models in a region
models = get_embedding_models_by_region("eu-central-1")
for model_id, cfg in models.items():
    print(f"{model_id}: {cfg.dimensions}")
```
