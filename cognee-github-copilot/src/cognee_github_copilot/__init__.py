"""
GitHub Copilot Adapter for Cognee

This package provides GitHub Copilot integration for Cognee,
supporting all GitHub Copilot Pro+ models from multiple providers:
- OpenAI (GPT-4.1, GPT-4o, GPT-5, o3, o4-mini)
- Anthropic (Claude Opus 4.1, Claude Sonnet 3.5/3.7/4)
- Google (Gemini 2.5 Pro, Gemini 2.0 Flash)
- xAI (Grok Code Fast 1)

Note: GitHub Copilot does not provide embedding models.
Configure embeddings separately using OpenAI, Cohere, or other providers.
"""

from .llm.github_copilot_llm_adapter import GitHubCopilotLLMAdapter
from .embedding.github_copilot_embedding_adapter import GitHubCopilotEmbeddingAdapter
from .register import register_github_copilot_adapters, get_github_copilot_config, get_github_copilot_adapters

__version__ = "0.1.0"

__all__ = [
    "GitHubCopilotLLMAdapter",
    "GitHubCopilotEmbeddingAdapter",
    "register_github_copilot_adapters",
    "get_github_copilot_config",
    "get_github_copilot_adapters",
]
