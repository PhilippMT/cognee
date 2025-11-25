"""
Configuration for AWS Bedrock foundation models available in EU regions.

This module provides comprehensive model information for all foundation models
available in AWS Bedrock for eu-central-1 and eu-north-1 regions, including
proper configuration for BAML with AWS Bedrock support.
"""

from typing import Dict, List, Literal
from dataclasses import dataclass


@dataclass
class ModelConfig:
    """Configuration for a Bedrock model."""

    model_id: str
    model_name: str
    provider: str
    regions: List[str]
    supports_tools: bool
    supports_streaming: bool
    input_modalities: List[str]
    output_modalities: List[str]
    max_tokens: int
    context_window: int
    recommended_mode: str  # For BAML: "tools" or "json"


# Anthropic Claude Models - Full tools support
CLAUDE_MODELS: Dict[str, ModelConfig] = {
    # Claude 3.5 Sonnet v2 - Latest generation
    "anthropic.claude-3-5-sonnet-20241022-v2:0": ModelConfig(
        model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
        model_name="Claude 3.5 Sonnet v2",
        provider="Anthropic",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=200000,
        recommended_mode="tools",
    ),
    # Claude 3.5 Sonnet v1
    "anthropic.claude-3-5-sonnet-20240620-v1:0": ModelConfig(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        model_name="Claude 3.5 Sonnet",
        provider="Anthropic",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=200000,
        recommended_mode="tools",
    ),
    # Claude 3.5 Haiku
    "anthropic.claude-3-5-haiku-20241022-v1:0": ModelConfig(
        model_id="anthropic.claude-3-5-haiku-20241022-v1:0",
        model_name="Claude 3.5 Haiku",
        provider="Anthropic",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=200000,
        recommended_mode="tools",
    ),
    # Claude 3 Sonnet
    "anthropic.claude-3-sonnet-20240229-v1:0": ModelConfig(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_name="Claude 3 Sonnet",
        provider="Anthropic",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=4096,
        context_window=200000,
        recommended_mode="tools",
    ),
    # Claude 3 Haiku
    "anthropic.claude-3-haiku-20240307-v1:0": ModelConfig(
        model_id="anthropic.claude-3-haiku-20240307-v1:0",
        model_name="Claude 3 Haiku",
        provider="Anthropic",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=4096,
        context_window=200000,
        recommended_mode="tools",
    ),
}


# Amazon Nova Models - Multimodal capabilities
AMAZON_NOVA_MODELS: Dict[str, ModelConfig] = {
    # Nova Pro
    "amazon.nova-pro-v1:0": ModelConfig(
        model_id="amazon.nova-pro-v1:0",
        model_name="Amazon Nova Pro",
        provider="Amazon",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE", "VIDEO"],
        output_modalities=["TEXT"],
        max_tokens=5120,
        context_window=300000,
        recommended_mode="tools",
    ),
    # Nova Lite
    "amazon.nova-lite-v1:0": ModelConfig(
        model_id="amazon.nova-lite-v1:0",
        model_name="Amazon Nova Lite",
        provider="Amazon",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE", "VIDEO"],
        output_modalities=["TEXT"],
        max_tokens=5120,
        context_window=300000,
        recommended_mode="tools",
    ),
    # Nova Micro
    "amazon.nova-micro-v1:0": ModelConfig(
        model_id="amazon.nova-micro-v1:0",
        model_name="Amazon Nova Micro",
        provider="Amazon",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=5120,
        context_window=128000,
        recommended_mode="tools",
    ),
}


# Meta Llama Models - Open source models
META_LLAMA_MODELS: Dict[str, ModelConfig] = {
    # Llama 3.3 70B Instruct
    "meta.llama3-3-70b-instruct-v1:0": ModelConfig(
        model_id="meta.llama3-3-70b-instruct-v1:0",
        model_name="Llama 3.3 70B Instruct",
        provider="Meta",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=2048,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Llama 3.2 90B Vision Instruct
    "meta.llama3-2-90b-instruct-v1:0": ModelConfig(
        model_id="meta.llama3-2-90b-instruct-v1:0",
        model_name="Llama 3.2 90B Vision Instruct",
        provider="Meta",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=2048,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Llama 3.2 11B Vision Instruct
    "meta.llama3-2-11b-instruct-v1:0": ModelConfig(
        model_id="meta.llama3-2-11b-instruct-v1:0",
        model_name="Llama 3.2 11B Vision Instruct",
        provider="Meta",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=2048,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Llama 3.2 3B Instruct
    "meta.llama3-2-3b-instruct-v1:0": ModelConfig(
        model_id="meta.llama3-2-3b-instruct-v1:0",
        model_name="Llama 3.2 3B Instruct",
        provider="Meta",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=2048,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Llama 3.2 1B Instruct
    "meta.llama3-2-1b-instruct-v1:0": ModelConfig(
        model_id="meta.llama3-2-1b-instruct-v1:0",
        model_name="Llama 3.2 1B Instruct",
        provider="Meta",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=2048,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Llama 3.1 405B Instruct
    "meta.llama3-1-405b-instruct-v1:0": ModelConfig(
        model_id="meta.llama3-1-405b-instruct-v1:0",
        model_name="Llama 3.1 405B Instruct",
        provider="Meta",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=2048,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Llama 3.1 70B Instruct
    "meta.llama3-1-70b-instruct-v1:0": ModelConfig(
        model_id="meta.llama3-1-70b-instruct-v1:0",
        model_name="Llama 3.1 70B Instruct",
        provider="Meta",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=2048,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Llama 3.1 8B Instruct
    "meta.llama3-1-8b-instruct-v1:0": ModelConfig(
        model_id="meta.llama3-1-8b-instruct-v1:0",
        model_name="Llama 3.1 8B Instruct",
        provider="Meta",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=2048,
        context_window=128000,
        recommended_mode="tools",
    ),
}


# Mistral Models
MISTRAL_MODELS: Dict[str, ModelConfig] = {
    # Mistral Large 2 (2407)
    "mistral.mistral-large-2407-v1:0": ModelConfig(
        model_id="mistral.mistral-large-2407-v1:0",
        model_name="Mistral Large 2 (2407)",
        provider="Mistral AI",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Mistral Large (2402)
    "mistral.mistral-large-2402-v1:0": ModelConfig(
        model_id="mistral.mistral-large-2402-v1:0",
        model_name="Mistral Large (2402)",
        provider="Mistral AI",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=32000,
        recommended_mode="tools",
    ),
    # Mistral Small
    "mistral.mistral-small-2402-v1:0": ModelConfig(
        model_id="mistral.mistral-small-2402-v1:0",
        model_name="Mistral Small (2402)",
        provider="Mistral AI",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=32000,
        recommended_mode="tools",
    ),
    # Mixtral 8x7B
    "mistral.mixtral-8x7b-instruct-v0:1": ModelConfig(
        model_id="mistral.mixtral-8x7b-instruct-v0:1",
        model_name="Mixtral 8x7B Instruct",
        provider="Mistral AI",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=4096,
        context_window=32000,
        recommended_mode="tools",
    ),
}


# Amazon Titan Models
AMAZON_TITAN_MODELS: Dict[str, ModelConfig] = {
    # Titan Text Premier
    "amazon.titan-text-premier-v1:0": ModelConfig(
        model_id="amazon.titan-text-premier-v1:0",
        model_name="Amazon Titan Text Premier",
        provider="Amazon",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=False,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=3072,
        context_window=32000,
        recommended_mode="json",
    ),
    # Titan Text Express
    "amazon.titan-text-express-v1": ModelConfig(
        model_id="amazon.titan-text-express-v1",
        model_name="Amazon Titan Text Express",
        provider="Amazon",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=False,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=8000,
        recommended_mode="json",
    ),
    # Titan Text Lite
    "amazon.titan-text-lite-v1": ModelConfig(
        model_id="amazon.titan-text-lite-v1",
        model_name="Amazon Titan Text Lite",
        provider="Amazon",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=False,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=4096,
        context_window=4000,
        recommended_mode="json",
    ),
}


# Cohere Models - Command R series
COHERE_MODELS: Dict[str, ModelConfig] = {
    # Command R+
    "cohere.command-r-plus-v1:0": ModelConfig(
        model_id="cohere.command-r-plus-v1:0",
        model_name="Command R+",
        provider="Cohere",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=4096,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Command R
    "cohere.command-r-v1:0": ModelConfig(
        model_id="cohere.command-r-v1:0",
        model_name="Command R",
        provider="Cohere",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=4096,
        context_window=128000,
        recommended_mode="tools",
    ),
}


# All models combined
ALL_MODELS: Dict[str, ModelConfig] = {
    **CLAUDE_MODELS,
    **AMAZON_NOVA_MODELS,
    **META_LLAMA_MODELS,
    **MISTRAL_MODELS,
    **AMAZON_TITAN_MODELS,
    **COHERE_MODELS,
}


# Cross-region inference profiles for EU
EU_CROSS_REGION_PROFILES: Dict[str, str] = {
    # Claude models
    "eu.anthropic.claude-3-5-sonnet-20241022-v2:0": "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "eu.anthropic.claude-3-5-sonnet-20240620-v1:0": "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "eu.anthropic.claude-3-5-haiku-20241022-v1:0": "anthropic.claude-3-5-haiku-20241022-v1:0",
    "eu.anthropic.claude-3-sonnet-20240229-v1:0": "anthropic.claude-3-sonnet-20240229-v1:0",
    "eu.anthropic.claude-3-haiku-20240307-v1:0": "anthropic.claude-3-haiku-20240307-v1:0",
    # Amazon Nova models
    "eu.amazon.nova-pro-v1:0": "amazon.nova-pro-v1:0",
    "eu.amazon.nova-lite-v1:0": "amazon.nova-lite-v1:0",
    "eu.amazon.nova-micro-v1:0": "amazon.nova-micro-v1:0",
    # Cohere models
    "eu.cohere.command-r-plus-v1:0": "cohere.command-r-plus-v1:0",
    "eu.cohere.command-r-v1:0": "cohere.command-r-v1:0",
}


def get_model_config(model_id: str) -> ModelConfig:
    """
    Get configuration for a specific model.

    Args:
        model_id: The model identifier (e.g., 'anthropic.claude-3-5-sonnet-20241022-v2:0')

    Returns:
        ModelConfig for the specified model

    Raises:
        ValueError: If model is not found
    """
    # Handle cross-region profiles
    if model_id.startswith("eu."):
        base_model = EU_CROSS_REGION_PROFILES.get(model_id)
        if base_model:
            model_id = base_model

    # Remove 'bedrock/' prefix if present
    if model_id.startswith("bedrock/"):
        model_id = model_id[8:]

    if model_id not in ALL_MODELS:
        raise ValueError(
            f"Model '{model_id}' not found in configuration. "
            f"Available models: {', '.join(ALL_MODELS.keys())}"
        )

    return ALL_MODELS[model_id]


def get_models_by_provider(provider: str) -> Dict[str, ModelConfig]:
    """Get all models from a specific provider."""
    return {
        model_id: config for model_id, config in ALL_MODELS.items() if config.provider == provider
    }


def get_models_by_region(region: str) -> Dict[str, ModelConfig]:
    """Get all models available in a specific region."""
    return {model_id: config for model_id, config in ALL_MODELS.items() if region in config.regions}


def get_models_with_tools_support() -> Dict[str, ModelConfig]:
    """Get all models that support tools/function calling."""
    return {model_id: config for model_id, config in ALL_MODELS.items() if config.supports_tools}


def get_recommended_mode(model_id: str) -> str:
    """
    Get the recommended BAML mode for a model.

    Args:
        model_id: The model identifier

    Returns:
        Recommended mode string (e.g., 'tools', 'json')
    """
    try:
        config = get_model_config(model_id)
        return config.recommended_mode
    except ValueError:
        # Default to json for unknown models
        return "json"
