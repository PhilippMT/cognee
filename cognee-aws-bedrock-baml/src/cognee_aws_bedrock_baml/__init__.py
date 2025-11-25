"""
AWS Bedrock Adapter for Cognee using BAML

This package provides AWS Bedrock foundation models integration for Cognee using BAML,
supporting LLMs, embeddings, and reranking models from Anthropic, Meta, Amazon, and Cohere.

BAML (Boundary ML) is a domain-specific language for building AI applications
with type-safe LLM interactions. This package uses BAML's aws-bedrock provider
for structured output generation.
"""

from .llm.baml_bedrock_llm_adapter import BamlBedrockLLMAdapter
from .embedding.baml_bedrock_embedding_adapter import BamlBedrockEmbeddingAdapter
from .register import register_baml_bedrock_adapters, get_baml_bedrock_config, get_baml_bedrock_adapters

__version__ = "0.1.0"

__all__ = [
    "BamlBedrockLLMAdapter",
    "BamlBedrockEmbeddingAdapter",
    "register_baml_bedrock_adapters",
    "get_baml_bedrock_config",
    "get_baml_bedrock_adapters",
]
