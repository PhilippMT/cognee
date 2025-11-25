"""
Registration module for AWS Bedrock BAML adapters.

This module provides functions to register AWS Bedrock LLM and embedding adapters
with the Cognee framework using BAML for LLM interactions.
"""

from typing import Optional, Dict, Any


# Global registry for Bedrock BAML adapters
_baml_bedrock_registry: Dict[str, Any] = {}


def register_baml_bedrock_adapters(
    llm_region: Optional[str] = None,
    llm_profile: Optional[str] = None,
    embedding_region: Optional[str] = None,
    embedding_profile: Optional[str] = None,
):
    """
    Register AWS Bedrock BAML adapters for LLM and embeddings with Cognee.

    This function registers the BamlBedrockLLMAdapter and BamlBedrockEmbeddingAdapter
    with Cognee's infrastructure, storing configuration for later use.

    BAML (Boundary ML) is a domain-specific language for building AI applications
    with type-safe LLM interactions. This integration uses BAML's aws-bedrock provider.

    Parameters:
    -----------
        llm_region (str, optional): AWS region for LLM (default: eu-central-1)
        llm_profile (str, optional): AWS profile for LLM
        embedding_region (str, optional): AWS region for embeddings (default: eu-central-1)
        embedding_profile (str, optional): AWS profile for embeddings

    Usage:
    ------
        from cognee_aws_bedrock_baml import register_baml_bedrock_adapters

        # Register with default settings
        register_baml_bedrock_adapters()

        # Register with custom regions and profiles
        register_baml_bedrock_adapters(
            llm_region="eu-west-1",
            llm_profile="my-llm-profile",
            embedding_region="eu-central-1",
            embedding_profile="my-embedding-profile"
        )

        # Configure and use - set provider to "aws_bedrock_baml"
        import cognee
        cognee.config.llm_provider = "aws_bedrock_baml"
        cognee.config.llm_model = "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"
        cognee.config.embedding_provider = "bedrock"
        cognee.config.embedding_model = "bedrock/amazon.titan-embed-text-v2:0"
    """
    from .llm.baml_bedrock_llm_adapter import BamlBedrockLLMAdapter
    from .embedding.baml_bedrock_embedding_adapter import BamlBedrockEmbeddingAdapter

    # Store configuration in registry
    _baml_bedrock_registry["config"] = {
        "llm_region": llm_region or "eu-central-1",
        "llm_profile": llm_profile,
        "embedding_region": embedding_region or "eu-central-1",
        "embedding_profile": embedding_profile,
    }

    _baml_bedrock_registry["llm_adapter"] = BamlBedrockLLMAdapter
    _baml_bedrock_registry["embedding_adapter"] = BamlBedrockEmbeddingAdapter

    print("✓ AWS Bedrock BAML adapters registered successfully")
    print(f"  LLM Region: {_baml_bedrock_registry['config']['llm_region']}")
    if _baml_bedrock_registry["config"]["llm_profile"]:
        print(f"  LLM Profile: {_baml_bedrock_registry['config']['llm_profile']}")
    print(f"  Embedding Region: {_baml_bedrock_registry['config']['embedding_region']}")
    if _baml_bedrock_registry["config"]["embedding_profile"]:
        print(f"  Embedding Profile: {_baml_bedrock_registry['config']['embedding_profile']}")

    print("\nTo use AWS Bedrock with BAML:")
    print("  1. Set cognee.config.llm_provider = 'aws_bedrock_baml'")
    print("  2. Set cognee.config.llm_model = 'bedrock/your-model-id'")
    print("  3. Set cognee.config.embedding_provider = 'bedrock'")
    print("  4. Set cognee.config.embedding_model = 'bedrock/your-embedding-model-id'")

    return _baml_bedrock_registry


def get_baml_bedrock_config() -> Dict[str, Any]:
    """
    Get the current Bedrock BAML configuration from the registry.

    Returns:
    --------
        Dict containing the Bedrock BAML configuration
    """
    return _baml_bedrock_registry.get("config", {})


def get_baml_bedrock_adapters() -> Dict[str, Any]:
    """
    Get registered Bedrock BAML adapter classes.

    Returns:
    --------
        Dict containing llm_adapter and embedding_adapter classes
    """
    return {
        "llm_adapter": _baml_bedrock_registry.get("llm_adapter"),
        "embedding_adapter": _baml_bedrock_registry.get("embedding_adapter"),
    }
