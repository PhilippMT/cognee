"""
Registration module for AWS Bedrock adapters.

This module provides functions to register AWS Bedrock LLM and embedding adapters
with the Cognee framework.
"""

from typing import Optional


def register_bedrock_adapters(
    llm_region: Optional[str] = None,
    llm_profile: Optional[str] = None,
    embedding_region: Optional[str] = None,
    embedding_profile: Optional[str] = None,
):
    """
    Register AWS Bedrock adapters for LLM and embeddings with Cognee.
    
    This function registers the BedrockLLMAdapter and BedrockEmbeddingAdapter
    with Cognee's infrastructure, allowing them to be used as providers.
    
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
        
        # Configure and use
        import cognee
        cognee.config.llm_provider = "aws_bedrock"
        cognee.config.llm_model = "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
        cognee.config.embedding_provider = "bedrock"
        cognee.config.embedding_model = "bedrock/amazon.titan-embed-text-v2:0"
    """
    from .llm.bedrock_llm_adapter import BedrockLLMAdapter
    from .embedding.bedrock_embedding_adapter import BedrockEmbeddingAdapter
    
    # Store configuration for later use
    _bedrock_config = {
        "llm_region": llm_region or "eu-central-1",
        "llm_profile": llm_profile,
        "embedding_region": embedding_region or "eu-central-1",
        "embedding_profile": embedding_profile,
    }
    
    # Register LLM adapter
    try:
        from cognee.infrastructure.llm.structured_output_framework.litellm_instructor.llm.get_llm_client import (
            LLMProvider,
        )
        
        # Add AWS_BEDROCK to the LLMProvider enum if not exists
        if not hasattr(LLMProvider, "AWS_BEDROCK"):
            LLMProvider.AWS_BEDROCK = "aws_bedrock"
            
    except Exception as e:
        print(f"Warning: Could not register LLM provider enum: {e}")
    
    # Store adapter classes for use by get_llm_client and get_embedding_engine
    # This allows the core framework to instantiate our adapters
    import sys
    if 'cognee_aws_bedrock_adapters' not in sys.modules:
        sys.modules['cognee_aws_bedrock_adapters'] = type(sys)('cognee_aws_bedrock_adapters')
    
    sys.modules['cognee_aws_bedrock_adapters'].BedrockLLMAdapter = BedrockLLMAdapter
    sys.modules['cognee_aws_bedrock_adapters'].BedrockEmbeddingAdapter = BedrockEmbeddingAdapter
    sys.modules['cognee_aws_bedrock_adapters'].config = _bedrock_config
    
    print("✓ AWS Bedrock adapters registered successfully")
    print(f"  LLM Region: {_bedrock_config['llm_region']}")
    if _bedrock_config['llm_profile']:
        print(f"  LLM Profile: {_bedrock_config['llm_profile']}")
    print(f"  Embedding Region: {_bedrock_config['embedding_region']}")
    if _bedrock_config['embedding_profile']:
        print(f"  Embedding Profile: {_bedrock_config['embedding_profile']}")
    
    return {
        "llm_adapter": BedrockLLMAdapter,
        "embedding_adapter": BedrockEmbeddingAdapter,
        "config": _bedrock_config,
    }
