"""GitHub Copilot Embedding Adapter for Cognee

Note: GitHub Copilot does not provide dedicated embedding models.
This module is provided for completeness in the adapter structure.

For embeddings, users should use:
- OpenAI embeddings (text-embedding-3-small, text-embedding-3-large)
- Cohere embeddings
- Other embedding providers supported by cognee

To use embeddings with GitHub Copilot LLMs:
1. Configure GitHub Copilot as your LLM provider
2. Configure a separate embedding provider (e.g., OpenAI, Cohere)

Example:
    import cognee
    from cognee_github_copilot import register_github_copilot_adapters
    
    # Register GitHub Copilot for LLM
    register_github_copilot_adapters()
    cognee.config.llm_provider = "github_copilot"
    cognee.config.llm_model = "gpt-4o"
    
    # Configure embeddings separately
    cognee.config.embedding_provider = "openai"
    cognee.config.embedding_model = "text-embedding-3-small"
"""

from cognee.shared.logging_utils import get_logger

logger = get_logger("GitHubCopilotEmbedding")


class GitHubCopilotEmbeddingAdapter:
    """
    Placeholder for GitHub Copilot Embedding Adapter.
    
    GitHub Copilot does not provide embedding models.
    Use OpenAI, Cohere, or other embedding providers instead.
    """

    def __init__(self, *args, **kwargs):
        """Initialize with error message."""
        raise NotImplementedError(
            "GitHub Copilot does not provide embedding models. "
            "Please use OpenAI, Cohere, or other embedding providers. "
            "Configure embeddings separately from your LLM provider."
        )
