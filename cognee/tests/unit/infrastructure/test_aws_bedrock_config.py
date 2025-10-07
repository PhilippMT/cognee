"""Unit tests for AWS Bedrock LLM configuration."""

import pytest
from unittest.mock import patch
from cognee.infrastructure.llm.config import LLMConfig


def test_aws_bedrock_config_defaults():
    """Test AWS Bedrock configuration with default values."""
    config = LLMConfig(
        llm_provider="aws_bedrock",
        llm_model="bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0",
    )
    
    assert config.llm_provider == "aws_bedrock"
    assert config.llm_model == "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
    assert config.aws_region_name is None
    assert config.aws_access_key_id is None
    assert config.aws_secret_access_key is None


def test_aws_bedrock_config_with_credentials():
    """Test AWS Bedrock configuration with explicit credentials."""
    config = LLMConfig(
        llm_provider="aws_bedrock",
        llm_model="bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0",
        aws_region_name="eu-central-1",
        aws_access_key_id="test_key",
        aws_secret_access_key="test_secret",
    )
    
    assert config.llm_provider == "aws_bedrock"
    assert config.aws_region_name == "eu-central-1"
    assert config.aws_access_key_id == "test_key"
    assert config.aws_secret_access_key == "test_secret"


def test_aws_bedrock_config_to_dict():
    """Test AWS Bedrock configuration serialization."""
    config = LLMConfig(
        llm_provider="aws_bedrock",
        llm_model="bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0",
        aws_region_name="eu-west-1",
        aws_access_key_id="test_key",
    )
    
    config_dict = config.to_dict()
    
    assert config_dict["provider"] == "aws_bedrock"
    assert config_dict["model"] == "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
    assert config_dict["aws_region_name"] == "eu-west-1"
    assert config_dict["aws_access_key_id"] == "test_key"


def test_aws_bedrock_cross_region_model():
    """Test AWS Bedrock configuration with cross-region inference profile."""
    config = LLMConfig(
        llm_provider="aws_bedrock",
        llm_model="bedrock/eu.anthropic.claude-3-7-sonnet-20250219-v1:0",
        aws_region_name="eu-central-1",
    )
    
    assert config.llm_model == "bedrock/eu.anthropic.claude-3-7-sonnet-20250219-v1:0"
    assert config.aws_region_name == "eu-central-1"


def test_aws_bedrock_with_fallback():
    """Test AWS Bedrock configuration with fallback model."""
    config = LLMConfig(
        llm_provider="aws_bedrock",
        llm_model="bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0",
        aws_region_name="eu-central-1",
        fallback_model="bedrock/anthropic.claude-3-haiku-20240307-v1:0",
        fallback_endpoint="eu-west-1",
    )
    
    assert config.fallback_model == "bedrock/anthropic.claude-3-haiku-20240307-v1:0"
    assert config.fallback_endpoint == "eu-west-1"


@pytest.mark.skipif(
    True,
    reason="BAML is optional and may not be installed",
)
def test_baml_aws_bedrock_config():
    """Test BAML framework configuration with AWS Bedrock."""
    config = LLMConfig(
        structured_output_framework="baml",
        baml_llm_provider="aws_bedrock",
        baml_llm_model="anthropic.claude-3-7-sonnet-20250219-v1:0",
        baml_llm_endpoint="eu-central-1",
    )
    
    assert config.structured_output_framework == "baml"
    assert config.baml_llm_provider == "aws_bedrock"
    assert config.baml_llm_model == "anthropic.claude-3-7-sonnet-20250219-v1:0"
    assert config.baml_llm_endpoint == "eu-central-1"


def test_aws_bedrock_with_profile():
    """Test AWS Bedrock configuration with named profile."""
    config = LLMConfig(
        llm_provider="aws_bedrock",
        llm_model="bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0",
        aws_region_name="eu-central-1",
        aws_profile_name="my-profile",
    )
    
    assert config.aws_profile_name == "my-profile"
    assert config.aws_region_name == "eu-central-1"


def test_aws_bedrock_backward_compatibility():
    """Test that AWS Bedrock can use legacy config fields."""
    config = LLMConfig(
        llm_provider="aws_bedrock",
        llm_model="bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0",
        llm_endpoint="eu-west-1",  # Legacy field
        llm_api_key="test_key",    # Legacy field for AWS key
        llm_api_version="test_secret",  # Legacy field for AWS secret
    )
    
    # Should still work with legacy fields
    assert config.llm_endpoint == "eu-west-1"
    assert config.llm_api_key == "test_key"
    assert config.llm_api_version == "test_secret"


def test_embedding_config_with_aws_bedrock():
    """Test embedding configuration with AWS Bedrock."""
    from cognee.infrastructure.databases.vector.embeddings.config import EmbeddingConfig
    
    config = EmbeddingConfig(
        embedding_provider="bedrock",
        embedding_model="bedrock/amazon.titan-embed-text-v2:0",
        embedding_dimensions=1024,
        aws_region_name="eu-central-1",
        aws_profile_name="my-profile",
    )
    
    assert config.embedding_provider == "bedrock"
    assert config.embedding_model == "bedrock/amazon.titan-embed-text-v2:0"
    assert config.embedding_dimensions == 1024
    assert config.aws_region_name == "eu-central-1"
    assert config.aws_profile_name == "my-profile"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
