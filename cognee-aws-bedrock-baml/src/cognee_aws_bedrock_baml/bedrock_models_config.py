"""
Configuration for AWS Bedrock foundation models available in EU regions.

This module provides comprehensive model information for all foundation models
available in AWS Bedrock for eu-central-1, eu-west-1, and eu-north-1 regions,
including proper configuration for BAML with AWS Bedrock support.

Last updated: December 2025 - Includes all latest models (Claude 4.x, Nova 2,
Qwen3, DeepSeek, Google Gemma, NVIDIA, Mistral Pixtral, etc.)
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class ModelConfig:
    """Configuration for a Bedrock LLM model."""

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


@dataclass
class EmbeddingModelConfig:
    """Configuration for a Bedrock Embedding model."""

    model_id: str
    model_name: str
    provider: str
    regions: List[str]
    dimensions: List[int]  # Available output dimensions
    default_dimensions: int
    max_input_tokens: int
    input_modalities: List[str]
    languages: List[str]


# =============================================================================
# ANTHROPIC CLAUDE MODELS
# =============================================================================
CLAUDE_MODELS: Dict[str, ModelConfig] = {
    # Claude Sonnet 4.5 - Latest flagship model (Dec 2025)
    "anthropic.claude-sonnet-4-5-20250929-v1:0": ModelConfig(
        model_id="anthropic.claude-sonnet-4-5-20250929-v1:0",
        model_name="Claude Sonnet 4.5",
        provider="Anthropic",
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=200000,
        recommended_mode="tools",
    ),
    # Claude Sonnet 4 (May 2025)
    "anthropic.claude-sonnet-4-20250514-v1:0": ModelConfig(
        model_id="anthropic.claude-sonnet-4-20250514-v1:0",
        model_name="Claude Sonnet 4",
        provider="Anthropic",
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=200000,
        recommended_mode="tools",
    ),
    # Claude Opus 4.5 (Nov 2025)
    "anthropic.claude-opus-4-5-20251101-v1:0": ModelConfig(
        model_id="anthropic.claude-opus-4-5-20251101-v1:0",
        model_name="Claude Opus 4.5",
        provider="Anthropic",
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=200000,
        recommended_mode="tools",
    ),
    # Claude Haiku 4.5 (Oct 2025)
    "anthropic.claude-haiku-4-5-20251001-v1:0": ModelConfig(
        model_id="anthropic.claude-haiku-4-5-20251001-v1:0",
        model_name="Claude Haiku 4.5",
        provider="Anthropic",
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=200000,
        recommended_mode="tools",
    ),
    # Claude 3.7 Sonnet (Feb 2025)
    "anthropic.claude-3-7-sonnet-20250219-v1:0": ModelConfig(
        model_id="anthropic.claude-3-7-sonnet-20250219-v1:0",
        model_name="Claude 3.7 Sonnet",
        provider="Anthropic",
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
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
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=200000,
        recommended_mode="tools",
    ),
    # Claude 3 Haiku
    "anthropic.claude-3-haiku-20240307-v1:0": ModelConfig(
        model_id="anthropic.claude-3-haiku-20240307-v1:0",
        model_name="Claude 3 Haiku",
        provider="Anthropic",
        regions=["eu-central-1", "eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=4096,
        context_window=200000,
        recommended_mode="tools",
    ),
}


# =============================================================================
# AMAZON NOVA MODELS
# =============================================================================
AMAZON_NOVA_MODELS: Dict[str, ModelConfig] = {
    # Nova 2 Lite - Latest generation (Dec 2025)
    "amazon.nova-2-lite-v1:0": ModelConfig(
        model_id="amazon.nova-2-lite-v1:0",
        model_name="Amazon Nova 2 Lite",
        provider="Amazon",
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE", "VIDEO"],
        output_modalities=["TEXT"],
        max_tokens=5120,
        context_window=300000,
        recommended_mode="tools",
    ),
    # Nova Pro
    "amazon.nova-pro-v1:0": ModelConfig(
        model_id="amazon.nova-pro-v1:0",
        model_name="Amazon Nova Pro",
        provider="Amazon",
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
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
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
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
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=5120,
        context_window=128000,
        recommended_mode="tools",
    ),
}


# =============================================================================
# META LLAMA MODELS
# =============================================================================
META_LLAMA_MODELS: Dict[str, ModelConfig] = {
    # Llama 3.2 3B Instruct (eu cross-region)
    "meta.llama3-2-3b-instruct-v1:0": ModelConfig(
        model_id="meta.llama3-2-3b-instruct-v1:0",
        model_name="Llama 3.2 3B Instruct",
        provider="Meta",
        regions=["eu-central-1", "eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=2048,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Llama 3.2 1B Instruct (eu cross-region)
    "meta.llama3-2-1b-instruct-v1:0": ModelConfig(
        model_id="meta.llama3-2-1b-instruct-v1:0",
        model_name="Llama 3.2 1B Instruct",
        provider="Meta",
        regions=["eu-central-1", "eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=2048,
        context_window=128000,
        recommended_mode="tools",
    ),
}


# =============================================================================
# MISTRAL AI MODELS
# =============================================================================
MISTRAL_MODELS: Dict[str, ModelConfig] = {
    # Pixtral Large 25.02 - Latest multimodal (Dec 2025)
    "mistral.pixtral-large-2502-v1:0": ModelConfig(
        model_id="mistral.pixtral-large-2502-v1:0",
        model_name="Pixtral Large (25.02)",
        provider="Mistral AI",
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Ministral 3 14B
    "mistral.ministral-3-14b-instruct": ModelConfig(
        model_id="mistral.ministral-3-14b-instruct",
        model_name="Ministral 14B 3.0",
        provider="Mistral AI",
        regions=["eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Ministral 3 8B
    "mistral.ministral-3-8b-instruct": ModelConfig(
        model_id="mistral.ministral-3-8b-instruct",
        model_name="Ministral 3 8B",
        provider="Mistral AI",
        regions=["eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Voxtral Small 24B 2507 - Audio capable
    "mistral.voxtral-small-24b-2507": ModelConfig(
        model_id="mistral.voxtral-small-24b-2507",
        model_name="Voxtral Small 24B 2507",
        provider="Mistral AI",
        regions=["eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["AUDIO", "TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=32000,
        recommended_mode="tools",
    ),
    # Voxtral Mini 3B 2507 - Audio capable
    "mistral.voxtral-mini-3b-2507": ModelConfig(
        model_id="mistral.voxtral-mini-3b-2507",
        model_name="Voxtral Mini 3B 2507",
        provider="Mistral AI",
        regions=["eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["AUDIO", "TEXT"],
        output_modalities=["TEXT"],
        max_tokens=4096,
        context_window=32000,
        recommended_mode="tools",
    ),
    # Mistral 7B Instruct
    "mistral.mistral-7b-instruct-v0:2": ModelConfig(
        model_id="mistral.mistral-7b-instruct-v0:2",
        model_name="Mistral 7B Instruct",
        provider="Mistral AI",
        regions=["eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=32000,
        recommended_mode="tools",
    ),
    # Mistral Large (24.02)
    "mistral.mistral-large-2402-v1:0": ModelConfig(
        model_id="mistral.mistral-large-2402-v1:0",
        model_name="Mistral Large (24.02)",
        provider="Mistral AI",
        regions=["eu-west-1"],
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
        regions=["eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=4096,
        context_window=32000,
        recommended_mode="tools",
    ),
}


# =============================================================================
# QWEN MODELS (Alibaba Cloud)
# =============================================================================
QWEN_MODELS: Dict[str, ModelConfig] = {
    # Qwen3 32B (Dense)
    "qwen.qwen3-32b-v1:0": ModelConfig(
        model_id="qwen.qwen3-32b-v1:0",
        model_name="Qwen3 32B",
        provider="Qwen",
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Qwen3 235B A22B 2507
    "qwen.qwen3-235b-a22b-2507-v1:0": ModelConfig(
        model_id="qwen.qwen3-235b-a22b-2507-v1:0",
        model_name="Qwen3 235B A22B 2507",
        provider="Qwen",
        regions=["eu-central-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Qwen3 Coder 30B A3B
    "qwen.qwen3-coder-30b-a3b-v1:0": ModelConfig(
        model_id="qwen.qwen3-coder-30b-a3b-v1:0",
        model_name="Qwen3 Coder 30B A3B",
        provider="Qwen",
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Qwen3 Coder 480B A35B
    "qwen.qwen3-coder-480b-a35b-v1:0": ModelConfig(
        model_id="qwen.qwen3-coder-480b-a35b-v1:0",
        model_name="Qwen3 Coder 480B A35B",
        provider="Qwen",
        regions=["eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Qwen3 Next 80B A3B
    "qwen.qwen3-next-80b-a3b": ModelConfig(
        model_id="qwen.qwen3-next-80b-a3b",
        model_name="Qwen3 Next 80B A3B",
        provider="Qwen",
        regions=["eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Qwen3 VL 235B A22B - Vision Language
    "qwen.qwen3-vl-235b-a22b": ModelConfig(
        model_id="qwen.qwen3-vl-235b-a22b",
        model_name="Qwen3 VL 235B A22B",
        provider="Qwen",
        regions=["eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
}


# =============================================================================
# OPENAI MODELS (Open source versions on Bedrock)
# =============================================================================
OPENAI_MODELS: Dict[str, ModelConfig] = {
    # GPT OSS 120B
    "openai.gpt-oss-120b-1:0": ModelConfig(
        model_id="openai.gpt-oss-120b-1:0",
        model_name="GPT OSS 120B",
        provider="OpenAI",
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
    # GPT OSS 20B
    "openai.gpt-oss-20b-1:0": ModelConfig(
        model_id="openai.gpt-oss-20b-1:0",
        model_name="GPT OSS 20B",
        provider="OpenAI",
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
    # GPT OSS Safeguard 120B
    "openai.gpt-oss-safeguard-120b": ModelConfig(
        model_id="openai.gpt-oss-safeguard-120b",
        model_name="GPT OSS Safeguard 120B",
        provider="OpenAI",
        regions=["eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
    # GPT OSS Safeguard 20B
    "openai.gpt-oss-safeguard-20b": ModelConfig(
        model_id="openai.gpt-oss-safeguard-20b",
        model_name="GPT OSS Safeguard 20B",
        provider="OpenAI",
        regions=["eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
}


# =============================================================================
# DEEPSEEK MODELS
# =============================================================================
DEEPSEEK_MODELS: Dict[str, ModelConfig] = {
    # DeepSeek-V3.1
    "deepseek.v3-v1:0": ModelConfig(
        model_id="deepseek.v3-v1:0",
        model_name="DeepSeek-V3.1",
        provider="DeepSeek",
        regions=["eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
}


# =============================================================================
# GOOGLE GEMMA MODELS
# =============================================================================
GOOGLE_MODELS: Dict[str, ModelConfig] = {
    # Gemma 3 27B IT
    "google.gemma-3-27b-it": ModelConfig(
        model_id="google.gemma-3-27b-it",
        model_name="Gemma 3 27B IT",
        provider="Google",
        regions=["eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Gemma 3 12B IT
    "google.gemma-3-12b-it": ModelConfig(
        model_id="google.gemma-3-12b-it",
        model_name="Gemma 3 12B IT",
        provider="Google",
        regions=["eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Gemma 3 4B IT
    "google.gemma-3-4b-it": ModelConfig(
        model_id="google.gemma-3-4b-it",
        model_name="Gemma 3 4B IT",
        provider="Google",
        regions=["eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
}


# =============================================================================
# NVIDIA MODELS
# =============================================================================
NVIDIA_MODELS: Dict[str, ModelConfig] = {
    # Nemotron Nano 12B v2 VL
    "nvidia.nemotron-nano-12b-v2": ModelConfig(
        model_id="nvidia.nemotron-nano-12b-v2",
        model_name="NVIDIA Nemotron Nano 12B v2 VL",
        provider="NVIDIA",
        regions=["eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "IMAGE"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
    # Nemotron Nano 9B v2
    "nvidia.nemotron-nano-9b-v2": ModelConfig(
        model_id="nvidia.nemotron-nano-9b-v2",
        model_name="NVIDIA Nemotron Nano 9B v2",
        provider="NVIDIA",
        regions=["eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
}


# =============================================================================
# MINIMAX MODELS
# =============================================================================
MINIMAX_MODELS: Dict[str, ModelConfig] = {
    # MiniMax M2
    "minimax.minimax-m2": ModelConfig(
        model_id="minimax.minimax-m2",
        model_name="MiniMax M2",
        provider="MiniMax",
        regions=["eu-west-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        max_tokens=8192,
        context_window=128000,
        recommended_mode="tools",
    ),
}


# =============================================================================
# TWELVELABS MODELS (Video Understanding)
# =============================================================================
TWELVELABS_MODELS: Dict[str, ModelConfig] = {
    # Pegasus v1.2
    "twelvelabs.pegasus-1-2-v1:0": ModelConfig(
        model_id="twelvelabs.pegasus-1-2-v1:0",
        model_name="Pegasus v1.2",
        provider="TwelveLabs",
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
        supports_tools=True,
        supports_streaming=True,
        input_modalities=["TEXT", "VIDEO"],
        output_modalities=["TEXT"],
        max_tokens=4096,
        context_window=64000,
        recommended_mode="tools",
    ),
}


# =============================================================================
# AMAZON TITAN TEXT MODELS (Legacy - removed from EU regions)
# =============================================================================
AMAZON_TITAN_MODELS: Dict[str, ModelConfig] = {}


# =============================================================================
# COHERE MODELS (LLM - removed from single-region EU)
# =============================================================================
COHERE_MODELS: Dict[str, ModelConfig] = {}


# =============================================================================
# AI21 MODELS (removed from EU regions)
# =============================================================================
AI21_MODELS: Dict[str, ModelConfig] = {}


# =============================================================================
# ALL LLM MODELS COMBINED
# =============================================================================
ALL_MODELS: Dict[str, ModelConfig] = {
    **CLAUDE_MODELS,
    **AMAZON_NOVA_MODELS,
    **META_LLAMA_MODELS,
    **MISTRAL_MODELS,
    **QWEN_MODELS,
    **OPENAI_MODELS,
    **DEEPSEEK_MODELS,
    **GOOGLE_MODELS,
    **NVIDIA_MODELS,
    **MINIMAX_MODELS,
    **TWELVELABS_MODELS,
    **AMAZON_TITAN_MODELS,
    **COHERE_MODELS,
    **AI21_MODELS,
}


# =============================================================================
# EMBEDDING MODELS
# =============================================================================
EMBEDDING_MODELS: Dict[str, EmbeddingModelConfig] = {
    # Amazon Titan Text Embeddings V2
    "amazon.titan-embed-text-v2:0": EmbeddingModelConfig(
        model_id="amazon.titan-embed-text-v2:0",
        model_name="Amazon Titan Text Embeddings V2",
        provider="Amazon",
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
        dimensions=[256, 512, 1024],
        default_dimensions=1024,
        max_input_tokens=8192,
        input_modalities=["TEXT"],
        languages=["100+ languages", "optimized for English"],
    ),
    # Amazon Titan Embeddings G1 - Text
    "amazon.titan-embed-text-v1": EmbeddingModelConfig(
        model_id="amazon.titan-embed-text-v1",
        model_name="Amazon Titan Embeddings G1 - Text",
        provider="Amazon",
        regions=["eu-central-1"],
        dimensions=[1536],
        default_dimensions=1536,
        max_input_tokens=8192,
        input_modalities=["TEXT"],
        languages=["English"],
    ),
    # Amazon Titan Multimodal Embeddings G1
    "amazon.titan-embed-image-v1": EmbeddingModelConfig(
        model_id="amazon.titan-embed-image-v1",
        model_name="Amazon Titan Multimodal Embeddings G1",
        provider="Amazon",
        regions=["eu-central-1", "eu-west-1"],
        dimensions=[256, 384, 1024],
        default_dimensions=1024,
        max_input_tokens=256,
        input_modalities=["TEXT", "IMAGE"],
        languages=["English"],
    ),
    # Cohere Embed v4 - Latest multimodal (Dec 2025)
    "cohere.embed-v4:0": EmbeddingModelConfig(
        model_id="cohere.embed-v4:0",
        model_name="Cohere Embed v4",
        provider="Cohere",
        regions=["eu-central-1", "eu-west-1", "eu-north-1"],
        dimensions=[256, 512, 1024, 1536],
        default_dimensions=1024,
        max_input_tokens=512,
        input_modalities=["TEXT", "IMAGE"],
        languages=["100+ languages"],
    ),
    # Cohere Embed English v3
    "cohere.embed-english-v3": EmbeddingModelConfig(
        model_id="cohere.embed-english-v3",
        model_name="Cohere Embed English v3",
        provider="Cohere",
        regions=["eu-central-1", "eu-west-1"],
        dimensions=[1024],
        default_dimensions=1024,
        max_input_tokens=512,
        input_modalities=["TEXT"],
        languages=["English"],
    ),
    # Cohere Embed Multilingual v3
    "cohere.embed-multilingual-v3": EmbeddingModelConfig(
        model_id="cohere.embed-multilingual-v3",
        model_name="Cohere Embed Multilingual v3",
        provider="Cohere",
        regions=["eu-central-1", "eu-west-1"],
        dimensions=[1024],
        default_dimensions=1024,
        max_input_tokens=512,
        input_modalities=["TEXT"],
        languages=["100+ languages"],
    ),
    # TwelveLabs Marengo Embed 3.0 - Video/Audio embedding
    "twelvelabs.marengo-embed-3-0-v1:0": EmbeddingModelConfig(
        model_id="twelvelabs.marengo-embed-3-0-v1:0",
        model_name="Marengo Embed 3.0",
        provider="TwelveLabs",
        regions=["eu-west-1"],
        dimensions=[1024],
        default_dimensions=1024,
        max_input_tokens=512,
        input_modalities=["TEXT", "IMAGE", "SPEECH", "VIDEO"],
        languages=["100+ languages"],
    ),
    # TwelveLabs Marengo Embed v2.7
    "twelvelabs.marengo-embed-2-7-v1:0": EmbeddingModelConfig(
        model_id="twelvelabs.marengo-embed-2-7-v1:0",
        model_name="Marengo Embed v2.7",
        provider="TwelveLabs",
        regions=["eu-west-1"],
        dimensions=[1024],
        default_dimensions=1024,
        max_input_tokens=512,
        input_modalities=["TEXT", "IMAGE", "SPEECH", "VIDEO"],
        languages=["100+ languages"],
    ),
    # Amazon Rerank 1.0
    "amazon.rerank-v1:0": EmbeddingModelConfig(
        model_id="amazon.rerank-v1:0",
        model_name="Amazon Rerank 1.0",
        provider="Amazon",
        regions=["eu-central-1"],
        dimensions=[1],  # Reranking returns scores, not embeddings
        default_dimensions=1,
        max_input_tokens=8192,
        input_modalities=["TEXT"],
        languages=["English"],
    ),
    # Cohere Rerank 3.5
    "cohere.rerank-v3-5:0": EmbeddingModelConfig(
        model_id="cohere.rerank-v3-5:0",
        model_name="Cohere Rerank 3.5",
        provider="Cohere",
        regions=["eu-central-1"],
        dimensions=[1],  # Reranking returns scores, not embeddings
        default_dimensions=1,
        max_input_tokens=4096,
        input_modalities=["TEXT"],
        languages=["100+ languages"],
    ),
}


# =============================================================================
# CROSS-REGION INFERENCE PROFILES FOR EU
# =============================================================================
EU_CROSS_REGION_PROFILES: Dict[str, str] = {
    # Claude models - Latest 4.x series
    "eu.anthropic.claude-sonnet-4-5-20250929-v1:0": "anthropic.claude-sonnet-4-5-20250929-v1:0",
    "eu.anthropic.claude-sonnet-4-20250514-v1:0": "anthropic.claude-sonnet-4-20250514-v1:0",
    "eu.anthropic.claude-opus-4-5-20251101-v1:0": "anthropic.claude-opus-4-5-20251101-v1:0",
    "eu.anthropic.claude-haiku-4-5-20251001-v1:0": "anthropic.claude-haiku-4-5-20251001-v1:0",
    "eu.anthropic.claude-3-7-sonnet-20250219-v1:0": "anthropic.claude-3-7-sonnet-20250219-v1:0",
    "eu.anthropic.claude-3-5-haiku-20241022-v1:0": "anthropic.claude-3-5-haiku-20241022-v1:0",
    "eu.anthropic.claude-3-haiku-20240307-v1:0": "anthropic.claude-3-haiku-20240307-v1:0",
    # Amazon Nova models
    "eu.amazon.nova-2-lite-v1:0": "amazon.nova-2-lite-v1:0",
    "eu.amazon.nova-pro-v1:0": "amazon.nova-pro-v1:0",
    "eu.amazon.nova-lite-v1:0": "amazon.nova-lite-v1:0",
    "eu.amazon.nova-micro-v1:0": "amazon.nova-micro-v1:0",
    # Meta Llama models
    "eu.meta.llama3-2-3b-instruct-v1:0": "meta.llama3-2-3b-instruct-v1:0",
    "eu.meta.llama3-2-1b-instruct-v1:0": "meta.llama3-2-1b-instruct-v1:0",
    # Mistral models
    "eu.mistral.pixtral-large-2502-v1:0": "mistral.pixtral-large-2502-v1:0",
    # Cohere Embed v4
    "eu.cohere.embed-v4:0": "cohere.embed-v4:0",
    # TwelveLabs Pegasus
    "eu.twelvelabs.pegasus-1-2-v1:0": "twelvelabs.pegasus-1-2-v1:0",
    # TwelveLabs Marengo
    "eu.twelvelabs.marengo-embed-2-7-v1:0": "twelvelabs.marengo-embed-2-7-v1:0",
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_model_config(model_id: str) -> ModelConfig:
    """
    Get configuration for a specific model.

    Args:
        model_id: The model identifier (e.g., 'anthropic.claude-sonnet-4-5-20250929-v1:0')

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
            f"Available models: {', '.join(sorted(ALL_MODELS.keys()))}"
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


# Embedding model helper functions
def get_embedding_model_config(model_id: str) -> EmbeddingModelConfig:
    """
    Get configuration for a specific embedding model.

    Args:
        model_id: The model identifier (e.g., 'amazon.titan-embed-text-v2:0')

    Returns:
        EmbeddingModelConfig for the specified model

    Raises:
        ValueError: If model is not found
    """
    # Remove 'bedrock/' prefix if present
    if model_id.startswith("bedrock/"):
        model_id = model_id[8:]

    if model_id not in EMBEDDING_MODELS:
        raise ValueError(
            f"Embedding model '{model_id}' not found in configuration. "
            f"Available models: {', '.join(sorted(EMBEDDING_MODELS.keys()))}"
        )

    return EMBEDDING_MODELS[model_id]


def get_embedding_models_by_region(region: str) -> Dict[str, EmbeddingModelConfig]:
    """Get all embedding models available in a specific region."""
    return {
        model_id: config
        for model_id, config in EMBEDDING_MODELS.items()
        if region in config.regions
    }


def get_all_embedding_models() -> Dict[str, EmbeddingModelConfig]:
    """Get all available embedding models."""
    return EMBEDDING_MODELS.copy()


def list_all_providers() -> List[str]:
    """Get a list of all model providers."""
    providers = set()
    for config in ALL_MODELS.values():
        providers.add(config.provider)
    for config in EMBEDDING_MODELS.values():
        providers.add(config.provider)
    return sorted(providers)
