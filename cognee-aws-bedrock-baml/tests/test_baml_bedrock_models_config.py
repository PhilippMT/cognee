"""
Tests for AWS Bedrock BAML model configuration

These tests verify the model configuration system without requiring
the full cognee installation or AWS credentials.
"""

import pytest

from cognee_aws_bedrock_baml.bedrock_models_config import (
    get_model_config,
    get_recommended_mode,
    get_embedding_model_config,
    get_embedding_models_by_region,
    ALL_MODELS,
    CLAUDE_MODELS,
    AMAZON_NOVA_MODELS,
    META_LLAMA_MODELS,
    MISTRAL_MODELS,
    AMAZON_TITAN_MODELS,
    COHERE_MODELS,
    AI21_MODELS,
    EMBEDDING_MODELS,
    EU_CROSS_REGION_PROFILES,
)


class TestModelConfiguration:
    """Test model configuration system."""

    def test_get_model_config_claude(self):
        """Test getting Claude model configuration."""
        config = get_model_config("anthropic.claude-3-5-sonnet-20241022-v2:0")
        assert config.model_id == "anthropic.claude-3-5-sonnet-20241022-v2:0"
        assert config.provider == "Anthropic"
        assert config.supports_tools is True
        assert config.recommended_mode == "tools"
        assert "eu-central-1" in config.regions
        assert "eu-west-1" in config.regions
        assert "eu-north-1" in config.regions

    def test_get_model_config_nova(self):
        """Test getting Amazon Nova model configuration."""
        config = get_model_config("amazon.nova-pro-v1:0")
        assert config.model_id == "amazon.nova-pro-v1:0"
        assert config.provider == "Amazon"
        assert config.supports_tools is True
        assert config.recommended_mode == "tools"
        assert "TEXT" in config.input_modalities
        assert "IMAGE" in config.input_modalities
        assert "VIDEO" in config.input_modalities

    def test_get_model_config_llama(self):
        """Test getting Llama model configuration."""
        config = get_model_config("meta.llama3-3-70b-instruct-v1:0")
        assert config.model_id == "meta.llama3-3-70b-instruct-v1:0"
        assert config.provider == "Meta"
        assert config.supports_tools is True
        assert config.recommended_mode == "tools"

    def test_get_model_config_titan_no_tools(self):
        """Test getting Titan model configuration (no tools support)."""
        config = get_model_config("amazon.titan-text-premier-v1:0")
        assert config.model_id == "amazon.titan-text-premier-v1:0"
        assert config.provider == "Amazon"
        assert config.supports_tools is False
        assert config.recommended_mode == "json"

    def test_get_model_config_ai21_jamba(self):
        """Test getting AI21 Jamba model configuration."""
        config = get_model_config("ai21.jamba-1-5-large-v1:0")
        assert config.model_id == "ai21.jamba-1-5-large-v1:0"
        assert config.provider == "AI21 Labs"
        assert config.supports_tools is True
        assert config.context_window == 256000

    def test_get_model_config_with_bedrock_prefix(self):
        """Test that bedrock/ prefix is properly handled."""
        config = get_model_config(
            "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"
        )
        assert config.model_id == "anthropic.claude-3-5-sonnet-20241022-v2:0"

    def test_get_model_config_cross_region_profile(self):
        """Test cross-region inference profile."""
        config = get_model_config("eu.anthropic.claude-3-5-sonnet-20241022-v2:0")
        assert config.model_id == "anthropic.claude-3-5-sonnet-20241022-v2:0"

    def test_get_model_config_invalid_model(self):
        """Test error handling for invalid model."""
        with pytest.raises(ValueError, match="Model .* not found"):
            get_model_config("invalid-model-id")

    def test_recommended_mode_tools_model(self):
        """Test recommended mode for tools-supporting model."""
        mode = get_recommended_mode("anthropic.claude-3-5-sonnet-20241022-v2:0")
        assert mode == "tools"

    def test_recommended_mode_json_only_model(self):
        """Test recommended mode for JSON-only model."""
        mode = get_recommended_mode("amazon.titan-text-premier-v1:0")
        assert mode == "json"

    def test_all_models_have_required_fields(self):
        """Test that all models have required configuration fields."""
        for model_id, config in ALL_MODELS.items():
            assert config.model_id == model_id
            assert config.provider
            assert config.regions
            assert isinstance(config.supports_tools, bool)
            assert isinstance(config.supports_streaming, bool)
            assert config.input_modalities
            assert config.output_modalities
            assert config.max_tokens > 0
            assert config.context_window > 0
            assert config.recommended_mode in [
                "tools",
                "json",
            ]

    def test_all_models_available_in_eu_regions(self):
        """Test that all models are available in target EU regions."""
        for model_id, config in ALL_MODELS.items():
            # All models should be available in at least one EU region
            eu_regions = ["eu-central-1", "eu-west-1", "eu-north-1"]
            has_eu_region = any(region in config.regions for region in eu_regions)
            assert (
                has_eu_region
            ), f"Model {model_id} not available in EU regions: {config.regions}"


class TestModelSupport:
    """Test that all documented models are properly supported."""

    def test_all_claude_models_configured(self):
        """Test that all Claude models are configured."""
        claude_model_ids = [
            "anthropic.claude-3-5-sonnet-20241022-v2:0",
            "anthropic.claude-3-5-sonnet-20240620-v1:0",
            "anthropic.claude-3-5-haiku-20241022-v1:0",
            "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-3-haiku-20240307-v1:0",
        ]
        for model_id in claude_model_ids:
            config = get_model_config(model_id)
            assert config.provider == "Anthropic"
            assert config.supports_tools is True

        # Verify count
        assert len(CLAUDE_MODELS) == 5

    def test_all_nova_models_configured(self):
        """Test that all Nova models are configured."""
        nova_model_ids = [
            "amazon.nova-pro-v1:0",
            "amazon.nova-lite-v1:0",
            "amazon.nova-micro-v1:0",
        ]
        for model_id in nova_model_ids:
            config = get_model_config(model_id)
            assert config.provider == "Amazon"
            assert config.supports_tools is True

        # Verify count
        assert len(AMAZON_NOVA_MODELS) == 3

    def test_all_llama_models_configured(self):
        """Test that all Llama models are configured."""
        llama_model_ids = [
            "meta.llama3-3-70b-instruct-v1:0",
            "meta.llama3-2-90b-instruct-v1:0",
            "meta.llama3-2-11b-instruct-v1:0",
            "meta.llama3-2-3b-instruct-v1:0",
            "meta.llama3-2-1b-instruct-v1:0",
            "meta.llama3-1-405b-instruct-v1:0",
            "meta.llama3-1-70b-instruct-v1:0",
            "meta.llama3-1-8b-instruct-v1:0",
        ]
        for model_id in llama_model_ids:
            config = get_model_config(model_id)
            assert config.provider == "Meta"
            assert config.supports_tools is True

        # Verify count
        assert len(META_LLAMA_MODELS) == 8

    def test_all_mistral_models_configured(self):
        """Test that all Mistral models are configured."""
        mistral_model_ids = [
            "mistral.mistral-large-2407-v1:0",
            "mistral.mistral-large-2402-v1:0",
            "mistral.mistral-small-2402-v1:0",
            "mistral.mixtral-8x7b-instruct-v0:1",
        ]
        for model_id in mistral_model_ids:
            config = get_model_config(model_id)
            assert config.provider == "Mistral AI"
            assert config.supports_tools is True

        # Verify count
        assert len(MISTRAL_MODELS) == 4

    def test_all_titan_models_configured(self):
        """Test that all Titan models are configured."""
        titan_model_ids = [
            "amazon.titan-text-premier-v1:0",
            "amazon.titan-text-express-v1",
            "amazon.titan-text-lite-v1",
        ]
        for model_id in titan_model_ids:
            config = get_model_config(model_id)
            assert config.provider == "Amazon"
            assert config.supports_tools is False  # Titan models don't support tools

        # Verify count
        assert len(AMAZON_TITAN_MODELS) == 3

    def test_all_cohere_models_configured(self):
        """Test that all Cohere models are configured."""
        cohere_model_ids = [
            "cohere.command-r-plus-v1:0",
            "cohere.command-r-v1:0",
        ]
        for model_id in cohere_model_ids:
            config = get_model_config(model_id)
            assert config.provider == "Cohere"
            assert config.supports_tools is True

        # Verify count
        assert len(COHERE_MODELS) == 2

    def test_all_ai21_models_configured(self):
        """Test that all AI21 Labs models are configured."""
        ai21_model_ids = [
            "ai21.jamba-1-5-large-v1:0",
            "ai21.jamba-1-5-mini-v1:0",
            "ai21.j2-ultra-v1",
            "ai21.j2-mid-v1",
        ]
        for model_id in ai21_model_ids:
            config = get_model_config(model_id)
            assert config.provider == "AI21 Labs"

        # Jamba models support tools, Jurassic-2 do not
        assert get_model_config("ai21.jamba-1-5-large-v1:0").supports_tools is True
        assert get_model_config("ai21.j2-ultra-v1").supports_tools is False

        # Verify count
        assert len(AI21_MODELS) == 4

    def test_total_model_count(self):
        """Test that we have the expected number of models."""
        # 5 Claude + 3 Nova + 8 Llama + 4 Mistral + 3 Titan + 2 Cohere + 4 AI21 = 29 models
        assert (
            len(ALL_MODELS) == 29
        ), f"Expected exactly 29 models, got {len(ALL_MODELS)}"

    def test_cross_region_profiles_exist(self):
        """Test that cross-region profiles are properly configured."""
        assert len(EU_CROSS_REGION_PROFILES) > 0

        # Test a few key profiles
        assert "eu.anthropic.claude-3-5-sonnet-20241022-v2:0" in EU_CROSS_REGION_PROFILES
        assert "eu.amazon.nova-pro-v1:0" in EU_CROSS_REGION_PROFILES
        assert "eu.cohere.command-r-plus-v1:0" in EU_CROSS_REGION_PROFILES


class TestModelCapabilities:
    """Test model capabilities and features."""

    def test_multimodal_models(self):
        """Test that multimodal models are properly identified."""
        # Nova models support text, image, and video
        nova_pro = get_model_config("amazon.nova-pro-v1:0")
        assert "TEXT" in nova_pro.input_modalities
        assert "IMAGE" in nova_pro.input_modalities
        assert "VIDEO" in nova_pro.input_modalities

        # Claude models support text and image
        claude = get_model_config("anthropic.claude-3-5-sonnet-20241022-v2:0")
        assert "TEXT" in claude.input_modalities
        assert "IMAGE" in claude.input_modalities

        # Llama vision models support text and image
        llama_vision = get_model_config("meta.llama3-2-90b-instruct-v1:0")
        assert "TEXT" in llama_vision.input_modalities
        assert "IMAGE" in llama_vision.input_modalities

    def test_context_windows(self):
        """Test that models have appropriate context windows."""
        # Nova has largest context (300K)
        nova = get_model_config("amazon.nova-pro-v1:0")
        assert nova.context_window == 300000

        # Jamba has 256K context
        jamba = get_model_config("ai21.jamba-1-5-large-v1:0")
        assert jamba.context_window == 256000

        # Claude 200K
        claude = get_model_config("anthropic.claude-3-5-sonnet-20241022-v2:0")
        assert claude.context_window == 200000

        # Llama and Cohere 128K
        llama = get_model_config("meta.llama3-3-70b-instruct-v1:0")
        assert llama.context_window == 128000

        cohere = get_model_config("cohere.command-r-plus-v1:0")
        assert cohere.context_window == 128000

    def test_tools_vs_json_models(self):
        """Test that models are correctly categorized for tools support."""
        tools_models_count = sum(
            1 for config in ALL_MODELS.values() if config.supports_tools
        )
        json_only_models_count = sum(
            1 for config in ALL_MODELS.values() if not config.supports_tools
        )

        # 24 models with tools (5 Claude + 3 Nova + 8 Llama + 4 Mistral + 2 Cohere + 2 Jamba)
        # 5 without tools (3 Titan + 2 Jurassic)
        assert tools_models_count == 24
        assert json_only_models_count == 5


class TestEmbeddingModels:
    """Test embedding model configuration."""

    def test_get_embedding_model_config(self):
        """Test getting embedding model configuration."""
        config = get_embedding_model_config("amazon.titan-embed-text-v2:0")
        assert config.model_id == "amazon.titan-embed-text-v2:0"
        assert config.provider == "Amazon"
        assert 1024 in config.dimensions
        assert config.default_dimensions == 1024

    def test_embedding_model_regions(self):
        """Test that embedding models are available in EU regions."""
        for model_id, config in EMBEDDING_MODELS.items():
            eu_regions = ["eu-central-1", "eu-west-1", "eu-north-1"]
            has_eu_region = any(region in config.regions for region in eu_regions)
            assert has_eu_region, f"Embedding model {model_id} not available in EU regions"

    def test_embedding_models_count(self):
        """Test that we have the expected number of embedding models."""
        assert len(EMBEDDING_MODELS) == 5

    def test_cohere_multilingual_embeddings(self):
        """Test Cohere multilingual embedding configuration."""
        config = get_embedding_model_config("cohere.embed-multilingual-v3")
        assert config.provider == "Cohere"
        assert "100+ languages" in config.languages

    def test_titan_multimodal_embeddings(self):
        """Test Titan multimodal embedding configuration."""
        config = get_embedding_model_config("amazon.titan-embed-image-v1")
        assert "IMAGE" in config.input_modalities
        assert "TEXT" in config.input_modalities

    def test_get_embedding_models_by_region(self):
        """Test filtering embedding models by region."""
        eu_central_models = get_embedding_models_by_region("eu-central-1")
        assert len(eu_central_models) == 5  # All should be available


class TestBAMLModeMapping:
    """Test BAML-specific mode mappings."""

    def test_baml_tools_mode(self):
        """Test that tools-supporting models use 'tools' mode for BAML."""
        tools_models = [
            "anthropic.claude-3-5-sonnet-20241022-v2:0",
            "amazon.nova-pro-v1:0",
            "meta.llama3-3-70b-instruct-v1:0",
            "mistral.mistral-large-2407-v1:0",
            "cohere.command-r-plus-v1:0",
            "ai21.jamba-1-5-large-v1:0",
        ]
        for model_id in tools_models:
            mode = get_recommended_mode(model_id)
            assert mode == "tools", f"Model {model_id} should use 'tools' mode"

    def test_baml_json_mode(self):
        """Test that JSON-only models use 'json' mode for BAML."""
        json_models = [
            "amazon.titan-text-premier-v1:0",
            "amazon.titan-text-express-v1",
            "amazon.titan-text-lite-v1",
            "ai21.j2-ultra-v1",
            "ai21.j2-mid-v1",
        ]
        for model_id in json_models:
            mode = get_recommended_mode(model_id)
            assert mode == "json", f"Model {model_id} should use 'json' mode"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
