# Quick Overview and Reference

## Supported Regions

| Region | Code | Location |
|--------|------|----------|
| Frankfurt | eu-central-1 | Germany |
| Ireland | eu-west-1 | Ireland |
| Stockholm | eu-north-1 | Sweden |

## Model Summary

### LLM Models with Tools Support

| Provider | Models | Best For |
|----------|--------|----------|
| **Anthropic Claude** | 5 models | Complex reasoning, multimodal |
| **Amazon Nova** | 3 models | Multimodal (text, image, video) |
| **Meta Llama** | 8 models | Open-source, customizable |
| **Mistral AI** | 4 models | European compliance |
| **Cohere** | 2 models | RAG, search, multilingual |
| **AI21 Labs** | 2 models (Jamba) | Long context (256K) |

### LLM Models without Tools Support (JSON mode)

| Provider | Models | Notes |
|----------|--------|-------|
| **Amazon Titan Text** | 3 models | AWS-native |
| **AI21 Jurassic-2** | 2 models | Text generation |

### Embedding Models

| Model | Dimensions | Languages |
|-------|------------|-----------|
| Titan Text Embeddings V2 | 256, 512, 1024 | 100+ |
| Titan Text Embeddings V1 | 1536 | English |
| Titan Multimodal G1 | 256, 384, 1024 | English |
| Cohere Embed English v3 | 1024 | English |
| Cohere Embed Multilingual v3 | 1024 | 100+ |

## Quick Configuration

### LLM Setup

```python
import cognee
cognee.config.llm_provider = "aws_bedrock_baml"
cognee.config.llm_model = "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"
cognee.config.aws_region_name = "eu-central-1"
```

### Embedding Setup

```python
cognee.config.embedding_provider = "bedrock"
cognee.config.embedding_model = "bedrock/amazon.titan-embed-text-v2:0"
cognee.config.embedding_dimensions = 1024
```

## Model Selection Guide

| Use Case | Recommended Model |
|----------|-------------------|
| Best overall | Claude 3.5 Sonnet v2 |
| Fast & cheap | Claude 3.5 Haiku or Nova Micro |
| Open source | Llama 3.3 70B |
| Long context | Jamba 1.5 Large (256K) |
| Multimodal | Nova Pro (text+image+video) |
| European compliance | Mistral Large 2 |
| RAG/Search | Command R+ |
