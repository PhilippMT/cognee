# AWS Bedrock Embedding Models - EU Regions

Complete catalog of embedding models available in eu-central-1, eu-west-1, and eu-north-1.

**Last Updated: December 2025**

## Model Summary

| Provider | Models | Dimensions | Modalities |
|----------|--------|------------|------------|
| Amazon Titan | 3 | 256-1536 | Text, Image |
| Cohere | 3 | 256-1536 | Text, Image |
| TwelveLabs | 2 | 1024 | Text, Image, Video, Speech |
| Rerankers | 2 | Scores | Text |

**Total: 10 Embedding/Rerank Models**

---

## Amazon Titan Embeddings

| Model ID | Name | Dimensions | Regions |
|----------|------|------------|---------|
| `amazon.titan-embed-text-v2:0` | Titan Text Embeddings V2 | 256, 512, 1024 | eu-central-1, eu-west-1, eu-north-1 |
| `amazon.titan-embed-text-v1` | Titan Embeddings G1 - Text | 1536 | eu-central-1 |
| `amazon.titan-embed-image-v1` | Titan Multimodal Embeddings G1 | 256, 384, 1024 | eu-central-1, eu-west-1 |

---

## Cohere Embeddings

| Model ID | Name | Dimensions | Languages | Modalities |
|----------|------|------------|-----------|------------|
| `cohere.embed-v4:0` | Cohere Embed v4 | 256-1536 | 100+ | Text, Image |
| `cohere.embed-english-v3` | Cohere Embed English v3 | 1024 | English | Text |
| `cohere.embed-multilingual-v3` | Cohere Embed Multilingual v3 | 1024 | 100+ | Text |

---

## TwelveLabs Marengo Embeddings

| Model ID | Name | Dimensions | Modalities |
|----------|------|------------|------------|
| `twelvelabs.marengo-embed-3-0-v1:0` | Marengo Embed 3.0 | 1024 | Text, Image, Speech, Video |
| `twelvelabs.marengo-embed-2-7-v1:0` | Marengo Embed v2.7 | 1024 | Text, Image, Speech, Video |

---

## Reranking Models

| Model ID | Name | Regions |
|----------|------|---------|
| `amazon.rerank-v1:0` | Amazon Rerank 1.0 | eu-central-1 |
| `cohere.rerank-v3-5:0` | Cohere Rerank 3.5 | eu-central-1 |

---

## Usage Examples

### Text Embeddings (Titan V2)

```python
from cognee_aws_bedrock_baml import BamlBedrockEmbeddingAdapter

# Amazon Titan V2 - Recommended for most use cases
adapter = BamlBedrockEmbeddingAdapter(
    model_id="amazon.titan-embed-text-v2:0",
    region_name="eu-central-1",
    dimensions=1024
)
```

### Multimodal Embeddings (Cohere v4)

```python
# Cohere Embed v4 - Best for text + image embeddings
adapter = BamlBedrockEmbeddingAdapter(
    model_id="cohere.embed-v4:0",
    region_name="eu-central-1"
)
```

### Video/Audio Embeddings (TwelveLabs)

```python
# TwelveLabs Marengo - For video and audio content
adapter = BamlBedrockEmbeddingAdapter(
    model_id="twelvelabs.marengo-embed-3-0-v1:0",
    region_name="eu-west-1"
)
```

---

## Model Selection Guide

| Use Case | Recommended Model |
|----------|-------------------|
| General text search | `amazon.titan-embed-text-v2:0` |
| Multilingual content | `cohere.embed-multilingual-v3` |
| Text + Image search | `cohere.embed-v4:0` |
| Video understanding | `twelvelabs.marengo-embed-3-0-v1:0` |
| Result reranking | `cohere.rerank-v3-5:0` |
| High dimension needs | `amazon.titan-embed-text-v1` (1536d) |
