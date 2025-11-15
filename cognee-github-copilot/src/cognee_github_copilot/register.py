"""
Registration module for GitHub Copilot adapters.

This module provides functions to register GitHub Copilot LLM adapters
with the Cognee framework using a cleaner registry pattern.
"""

from typing import Optional, Dict, Any


# Global registry for GitHub Copilot adapters
_github_copilot_registry: Dict[str, Any] = {}


def register_github_copilot_adapters(
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
):
    """
    Register GitHub Copilot adapters for LLM with Cognee.
    
    This function registers the GitHubCopilotLLMAdapter with Cognee's infrastructure,
    storing configuration for later use.
    
    Parameters:
    -----------
        api_key (str, optional): GitHub Copilot API key (uses GITHUB_TOKEN from environment if not provided)
        endpoint (str, optional): Custom endpoint URL for GitHub Copilot API
        
    Usage:
    ------
        from cognee_github_copilot import register_github_copilot_adapters
        
        # Register with default settings
        register_github_copilot_adapters()
        
        # Register with custom API key
        register_github_copilot_adapters(
            api_key="your-github-token"
        )
        
        # Configure and use - set provider to "github_copilot"
        import cognee
        cognee.config.llm_provider = "github_copilot"
        cognee.config.llm_model = "gpt-4o"
        
        # Note: GitHub Copilot does not provide embeddings
        # Configure embeddings separately
        cognee.config.embedding_provider = "openai"
        cognee.config.embedding_model = "text-embedding-3-small"
    """
    from .llm.github_copilot_llm_adapter import GitHubCopilotLLMAdapter
    
    # Store configuration in registry
    _github_copilot_registry["config"] = {
        "api_key": api_key,
        "endpoint": endpoint,
    }
    
    _github_copilot_registry["llm_adapter"] = GitHubCopilotLLMAdapter
    
    print("✓ GitHub Copilot adapters registered successfully")
    if api_key:
        print(f"  API Key: {'*' * (len(api_key) - 4)}{api_key[-4:]}")
    else:
        print("  API Key: Using GITHUB_TOKEN from environment")
    if endpoint:
        print(f"  Endpoint: {endpoint}")
    
    print("\nTo use GitHub Copilot:")
    print("  1. Set cognee.config.llm_provider = 'github_copilot'")
    print("  2. Set cognee.config.llm_model = 'gpt-4o' (or any supported model)")
    print("\nSupported models:")
    print("  OpenAI: gpt-4.1, gpt-4o, gpt-5, gpt-5-mini, o3, o4-mini")
    print("  Anthropic: claude-opus-4.1, claude-opus-4, claude-sonnet-3.5, claude-sonnet-3.7, claude-sonnet-4")
    print("  Google: gemini-2.5-pro, gemini-2.0-flash")
    print("  xAI: grok-code-fast-1")
    print("\nNote: GitHub Copilot does not provide embeddings.")
    print("Configure embeddings separately (e.g., OpenAI, Cohere)")
    
    return _github_copilot_registry


def get_github_copilot_config() -> Dict[str, Any]:
    """
    Get the current GitHub Copilot configuration from the registry.
    
    Returns:
    --------
        Dict containing the GitHub Copilot configuration
    """
    return _github_copilot_registry.get("config", {})


def get_github_copilot_adapters() -> Dict[str, Any]:
    """
    Get registered GitHub Copilot adapter classes.
    
    Returns:
    --------
        Dict containing llm_adapter class
    """
    return {
        "llm_adapter": _github_copilot_registry.get("llm_adapter"),
    }
