"""
AWS Bedrock Adapter for Cognee

This package provides AWS Bedrock foundation models integration for Cognee,
supporting LLMs, embeddings, and reranking models from Anthropic, Meta, Amazon, and Cohere.
"""

from .llm.bedrock_llm_adapter import BedrockLLMAdapter
from .embedding.bedrock_embedding_adapter import BedrockEmbeddingAdapter
from .register import register_bedrock_adapters, get_bedrock_config, get_bedrock_adapters

__version__ = "0.1.0"

__all__ = [
    "BedrockLLMAdapter",
    "BedrockEmbeddingAdapter",
    "register_bedrock_adapters",
    "get_bedrock_config",
    "get_bedrock_adapters",
]
