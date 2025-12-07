"""
Tests for AWS Bedrock BAML model configuration

These tests verify the model configuration system without requiring
the full cognee installation or AWS credentials.

Updated: December 2025 - Tests for new models (Claude 4.x, Nova 2, Qwen3, etc.)
"""

import pytest

from cognee_aws_bedrock_baml.bedrock_models_config import (
    get_model_config,
    get_recommended_mode,
    get_embedding_model_config,
    get_embedding_models_by_region,
    get_models_by_region,
    get_models_by_provider,
    list_all_providers,
    ALL_MODELS,
    CLAUDE_MODELS,
    AMAZON_NOVA_MODELS,
    META_LLAMA_MODELS,
    MISTRAL_MODELS,
    QWEN_MODELS,
    OPENAI_MODELS,
    DEEPSEEK_MODELS,
    GOOGLE_MODELS,
    NVIDIA_MODELS,
    MINIMAX_MODELS,
    TWELVELABS_MODELS,
    EMBEDDING_MODELS,
    EU_CROSS_REGION_PROFILES,
)


class TestModelConfiguration:
    """Test model configuration system."""

    def test_get_model_config_claude_sonnet_45(self):
        """Test getting latest Claude Sonnet 4.5 model configuration."""
        config = get_model_config("anthropic.claude-sonnet-4-5-20250929-v1:0")
        assert config.model_id == "anthropic.claude-sonnet-4-5-20250929-v1:0"
        assert config.provider == "Anthropic"
        assert config.supports_tools is True
        assert config.recommended_mode == "tools"
        assert "eu-central-1" in config.regions
        assert "eu-west-1" in config.regions
        assert "eu-north-1" in config.regions

    def test_get_model_config_nova_2_lite(self):
        """Test getting Amazon Nova 2 Lite model configuration."""
        config = get_model_config("amazon.nova-2-lite-v1:0")
        assert config.model_id == "amazon.nova-2-lite-v1:0"
        assert config.provider == "Amazon"
        assert config.supports_tools is True
        assert config.recommended_mode == "tools"
        assert "TEXT" in config.input_modalities
        assert "IMAGE" in config.input_modalities
        assert "VIDEO" in config.input_modalities

    def test_get_model_config_qwen3(self):
        """Test getting Qwen3 model configuration."""
        config = get_model_config("qwen.qwen3-32b-v1:0")
        assert config.model_id == "qwen.qwen3-32b-v1:0"
        assert config.provider == "Qwen"
        assert config.supports_tools is True
        assert config.recommended_mode == "tools"

    def test_get_model_config_pixtral_large(self):
        """Test getting Mistral Pixtral Large model configuration."""
        config = get_model_config("mistral.pixtral-large-2502-v1:0")
        assert config.model_id == "mistral.pixtral-large-2502-v1:0"
        assert config.provider == "Mistral AI"
        assert config.supports_tools is True
        assert "IMAGE" in config.input_modalities

    def test_get_model_config_openai_gpt_oss(self):
        """Test getting OpenAI GPT OSS model configuration."""
        config = get_model_config("openai.gpt-oss-120b-1:0")
        assert config.model_id == "openai.gpt-oss-120b-1:0"
        assert config.provider == "OpenAI"
        assert config.supports_tools is True

    def test_get_model_config_with_bedrock_prefix(self):
        """Test that bedrock/ prefix is properly handled."""
        config = get_model_config(
            "bedrock/anthropic.claude-sonnet-4-5-20250929-v1:0"
        )
        assert config.model_id == "anthropic.claude-sonnet-4-5-20250929-v1:0"

    def test_get_model_config_cross_region_profile(self):
        """Test cross-region inference profile."""
        config = get_model_config("eu.anthropic.claude-sonnet-4-5-20250929-v1:0")
        assert config.model_id == "anthropic.claude-sonnet-4-5-20250929-v1:0"

    def test_get_model_config_invalid_model(self):
        """Test error handling for invalid model."""
        with pytest.raises(ValueError, match="Model .* not found"):
            get_model_config("invalid-model-id")

    def test_recommended_mode_tools_model(self):
        """Test recommended mode for tools-supporting model."""
        mode = get_recommended_mode("anthropic.claude-sonnet-4-5-20250929-v1:0")
        assert mode == "tools"

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


class TestNewModelProviders:
    """Test configuration for new model providers."""

    def test_claude_models_count(self):
        """Test that Claude models are configured."""
        assert len(CLAUDE_MODELS) >= 5  # At least 5 Claude models

    def test_nova_models_count(self):
        """Test that Nova models are configured."""
        assert len(AMAZON_NOVA_MODELS) >= 4  # Nova 2 Lite, Pro, Lite, Micro

    def test_qwen_models_count(self):
        """Test that Qwen models are configured."""
        assert len(QWEN_MODELS) >= 4  # Multiple Qwen3 models

    def test_openai_models_count(self):
        """Test that OpenAI OSS models are configured."""
        assert len(OPENAI_MODELS) >= 2  # GPT OSS 120B and 20B

    def test_google_models_count(self):
        """Test that Google Gemma models are configured."""
        assert len(GOOGLE_MODELS) >= 3  # Gemma 3 4B, 12B, 27B

    def test_nvidia_models_count(self):
        """Test that NVIDIA models are configured."""
        assert len(NVIDIA_MODELS) >= 2  # Nemotron Nano models

    def test_deepseek_models_count(self):
        """Test that DeepSeek models are configured."""
        assert len(DEEPSEEK_MODELS) >= 1  # DeepSeek V3.1

    def test_twelvelabs_models_count(self):
        """Test that TwelveLabs models are configured."""
        assert len(TWELVELABS_MODELS) >= 1  # Pegasus v1.2

    def test_total_model_count(self):
        """Test that we have the expected minimum number of models."""
        # Should have 35+ models with all the new providers
        assert len(ALL_MODELS) >= 35, f"Expected at least 35 models, got {len(ALL_MODELS)}"

    def test_cross_region_profiles_exist(self):
        """Test that cross-region profiles are properly configured."""
        assert len(EU_CROSS_REGION_PROFILES) > 0
        # Test key profiles
        assert "eu.anthropic.claude-sonnet-4-5-20250929-v1:0" in EU_CROSS_REGION_PROFILES
        assert "eu.amazon.nova-2-lite-v1:0" in EU_CROSS_REGION_PROFILES


class TestModelCapabilities:
    """Test model capabilities and features."""

    def test_multimodal_models(self):
        """Test that multimodal models are properly identified."""
        # Nova 2 Lite supports text, image, and video
        nova_2_lite = get_model_config("amazon.nova-2-lite-v1:0")
        assert "TEXT" in nova_2_lite.input_modalities
        assert "IMAGE" in nova_2_lite.input_modalities
        assert "VIDEO" in nova_2_lite.input_modalities

        # Claude Sonnet 4.5 supports text and image
        claude = get_model_config("anthropic.claude-sonnet-4-5-20250929-v1:0")
        assert "TEXT" in claude.input_modalities
        assert "IMAGE" in claude.input_modalities

        # Qwen VL supports text and image
        if "qwen.qwen3-vl-235b-a22b" in ALL_MODELS:
            qwen_vl = get_model_config("qwen.qwen3-vl-235b-a22b")
            assert "IMAGE" in qwen_vl.input_modalities

    def test_audio_capable_models(self):
        """Test models with audio input support."""
        # Voxtral models support audio
        voxtral = get_model_config("mistral.voxtral-small-24b-2507")
        assert "AUDIO" in voxtral.input_modalities

    def test_video_understanding_models(self):
        """Test models with video understanding."""
        pegasus = get_model_config("twelvelabs.pegasus-1-2-v1:0")
        assert "VIDEO" in pegasus.input_modalities

    def test_context_windows(self):
        """Test that models have appropriate context windows."""
        # Nova 2 Lite has largest context (300K)
        nova = get_model_config("amazon.nova-2-lite-v1:0")
        assert nova.context_window == 300000

        # Claude 4.5 200K
        claude = get_model_config("anthropic.claude-sonnet-4-5-20250929-v1:0")
        assert claude.context_window == 200000

        # Qwen 128K
        qwen = get_model_config("qwen.qwen3-32b-v1:0")
        assert qwen.context_window == 128000

    def test_all_models_support_tools(self):
        """Test that all new models support tools."""
        # All new models should support tools
        tools_count = sum(1 for config in ALL_MODELS.values() if config.supports_tools)
        # Most models should support tools (at least 90%)
        assert tools_count >= len(ALL_MODELS) * 0.9


class TestEmbeddingModels:
    """Test embedding model configuration."""

    def test_get_embedding_model_config_cohere_v4(self):
        """Test getting Cohere Embed v4 configuration."""
        config = get_embedding_model_config("cohere.embed-v4:0")
        assert config.model_id == "cohere.embed-v4:0"
        assert config.provider == "Cohere"
        assert 1024 in config.dimensions
        assert "IMAGE" in config.input_modalities  # Multimodal

    def test_get_embedding_model_titan_v2(self):
        """Test getting Titan Embeddings V2 configuration."""
        config = get_embedding_model_config("amazon.titan-embed-text-v2:0")
        assert config.model_id == "amazon.titan-embed-text-v2:0"
        assert config.provider == "Amazon"
        assert config.default_dimensions == 1024

    def test_twelvelabs_marengo_embeddings(self):
        """Test TwelveLabs Marengo embedding configuration."""
        config = get_embedding_model_config("twelvelabs.marengo-embed-3-0-v1:0")
        assert config.provider == "TwelveLabs"
        assert "VIDEO" in config.input_modalities
        assert "SPEECH" in config.input_modalities

    def test_embedding_model_regions(self):
        """Test that embedding models are available in EU regions."""
        for model_id, config in EMBEDDING_MODELS.items():
            eu_regions = ["eu-central-1", "eu-west-1", "eu-north-1"]
            has_eu_region = any(region in config.regions for region in eu_regions)
            assert has_eu_region, f"Embedding model {model_id} not available in EU regions"

    def test_embedding_models_count(self):
        """Test that we have the expected number of embedding models."""
        assert len(EMBEDDING_MODELS) >= 8  # Multiple embedding models including rerankers

    def test_rerank_models(self):
        """Test that rerank models are configured."""
        amazon_rerank = get_embedding_model_config("amazon.rerank-v1:0")
        assert amazon_rerank.provider == "Amazon"
        
        cohere_rerank = get_embedding_model_config("cohere.rerank-v3-5:0")
        assert cohere_rerank.provider == "Cohere"

    def test_get_embedding_models_by_region(self):
        """Test filtering embedding models by region."""
        eu_central_models = get_embedding_models_by_region("eu-central-1")
        assert len(eu_central_models) >= 4  # Multiple should be available


class TestRegionSupport:
    """Test region-specific model availability."""

    def test_eu_central_1_models(self):
        """Test models available in eu-central-1."""
        models = get_models_by_region("eu-central-1")
        assert len(models) >= 10  # Multiple models available

    def test_eu_west_1_models(self):
        """Test models available in eu-west-1."""
        models = get_models_by_region("eu-west-1")
        assert len(models) >= 10  # Multiple models available

    def test_eu_north_1_models(self):
        """Test models available in eu-north-1."""
        models = get_models_by_region("eu-north-1")
        assert len(models) >= 5  # Some models available


class TestProviderHelper:
    """Test provider helper functions."""

    def test_list_all_providers(self):
        """Test listing all providers."""
        providers = list_all_providers()
        assert "Anthropic" in providers
        assert "Amazon" in providers
        assert "Qwen" in providers
        assert "OpenAI" in providers
        assert "Google" in providers

    def test_get_models_by_provider_anthropic(self):
        """Test getting Anthropic models."""
        models = get_models_by_provider("Anthropic")
        assert len(models) >= 5


class TestBAMLModeMapping:
    """Test BAML-specific mode mappings."""

    def test_baml_tools_mode(self):
        """Test that tools-supporting models use 'tools' mode for BAML."""
        tools_models = [
            "anthropic.claude-sonnet-4-5-20250929-v1:0",
            "amazon.nova-2-lite-v1:0",
            "qwen.qwen3-32b-v1:0",
            "mistral.pixtral-large-2502-v1:0",
            "openai.gpt-oss-120b-1:0",
        ]
        for model_id in tools_models:
            mode = get_recommended_mode(model_id)
            assert mode == "tools", f"Model {model_id} should use 'tools' mode"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
