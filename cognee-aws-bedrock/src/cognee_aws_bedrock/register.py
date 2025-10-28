"""
Registration module for AWS Bedrock adapters.

This module provides functions to register AWS Bedrock LLM and embedding adapters
with the Cognee framework using a cleaner registry pattern.
"""

from typing import Optional, Dict, Any


# Global registry for Bedrock adapters
_bedrock_registry: Dict[str, Any] = {}


def register_bedrock_adapters(
    llm_region: Optional[str] = None,
    llm_profile: Optional[str] = None,
    embedding_region: Optional[str] = None,
    embedding_profile: Optional[str] = None,
):
    """
    Register AWS Bedrock adapters for LLM and embeddings with Cognee.
    
    This function registers the BedrockLLMAdapter and BedrockEmbeddingAdapter
    with Cognee's infrastructure, storing configuration for later use.
    
    Parameters:
    -----------
        llm_region (str, optional): AWS region for LLM (default: eu-central-1)
        llm_profile (str, optional): AWS profile for LLM
        embedding_region (str, optional): AWS region for embeddings (default: eu-central-1)
        embedding_profile (str, optional): AWS profile for embeddings
        
    Usage:
    ------
        from cognee_aws_bedrock import register_bedrock_adapters
        
        # Register with default settings
        register_bedrock_adapters()
        
        # Register with custom regions and profiles
        register_bedrock_adapters(
            llm_region="eu-west-1",
            llm_profile="my-llm-profile",
            embedding_region="eu-central-1",
            embedding_profile="my-embedding-profile"
        )
        
        # Configure and use - set provider to "aws_bedrock"
        import cognee
        cognee.config.llm_provider = "aws_bedrock"
        cognee.config.llm_model = "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
        cognee.config.embedding_provider = "bedrock"
        cognee.config.embedding_model = "bedrock/amazon.titan-embed-text-v2:0"
    """
    from .llm.bedrock_llm_adapter import BedrockLLMAdapter
    from .embedding.bedrock_embedding_adapter import BedrockEmbeddingAdapter
    
    # Store configuration in registry
    _bedrock_registry["config"] = {
        "llm_region": llm_region or "eu-central-1",
        "llm_profile": llm_profile,
        "embedding_region": embedding_region or "eu-central-1",
        "embedding_profile": embedding_profile,
    }
    
    _bedrock_registry["llm_adapter"] = BedrockLLMAdapter
    _bedrock_registry["embedding_adapter"] = BedrockEmbeddingAdapter
    
    print("✓ AWS Bedrock adapters registered successfully")
    print(f"  LLM Region: {_bedrock_registry['config']['llm_region']}")
    if _bedrock_registry['config']['llm_profile']:
        print(f"  LLM Profile: {_bedrock_registry['config']['llm_profile']}")
    print(f"  Embedding Region: {_bedrock_registry['config']['embedding_region']}")
    if _bedrock_registry['config']['embedding_profile']:
        print(f"  Embedding Profile: {_bedrock_registry['config']['embedding_profile']}")
    
    print("\nTo use AWS Bedrock:")
    print("  1. Set cognee.config.llm_provider = 'aws_bedrock'")
    print("  2. Set cognee.config.llm_model = 'bedrock/your-model-id'")
    print("  3. Set cognee.config.embedding_provider = 'bedrock'")
    print("  4. Set cognee.config.embedding_model = 'bedrock/your-embedding-model-id'")
    
    return _bedrock_registry


def get_bedrock_config() -> Dict[str, Any]:
    """
    Get the current Bedrock configuration from the registry.
    
    Returns:
    --------
        Dict containing the Bedrock configuration
    """
    return _bedrock_registry.get("config", {})


def get_bedrock_adapters() -> Dict[str, Any]:
    """
    Get registered Bedrock adapter classes.
    
    Returns:
    --------
        Dict containing llm_adapter and embedding_adapter classes
    """
    return {
        "llm_adapter": _bedrock_registry.get("llm_adapter"),
        "embedding_adapter": _bedrock_registry.get("embedding_adapter"),
    }
