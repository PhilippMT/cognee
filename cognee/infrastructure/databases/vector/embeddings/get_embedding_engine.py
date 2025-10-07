from cognee.infrastructure.databases.vector.embeddings.config import get_embedding_config
from cognee.infrastructure.llm.config import (
    get_llm_config,
)
from .EmbeddingEngine import EmbeddingEngine
from functools import lru_cache


def get_embedding_engine() -> EmbeddingEngine:
    """
    Retrieve the embedding engine singleton based on configuration.

    This function calls the configuration retrieval functions to get the necessary settings
    for the embedding engine and creates a singleton instance. This ensures that too many
    requests won't be sent to HuggingFace by reusing the same instance for subsequent calls.

    Returns:
    --------

        - EmbeddingEngine: An instance of the embedding engine configured based on the
          retrieved settings.
    """
    config = get_embedding_config()
    llm_config = get_llm_config()
    # Embedding engine has to be a singleton based on configuration to ensure too many requests won't be sent to HuggingFace
    return create_embedding_engine(
        config.embedding_provider,
        config.embedding_model,
        config.embedding_dimensions,
        config.embedding_max_completion_tokens,
        config.embedding_endpoint,
        config.embedding_api_key,
        config.embedding_api_version,
        config.huggingface_tokenizer,
        llm_config.llm_api_key,
        llm_config.llm_provider,
        config.aws_region_name,
        config.aws_access_key_id,
        config.aws_secret_access_key,
        config.aws_profile_name,
    )


@lru_cache
def create_embedding_engine(
    embedding_provider,
    embedding_model,
    embedding_dimensions,
    embedding_max_completion_tokens,
    embedding_endpoint,
    embedding_api_key,
    embedding_api_version,
    huggingface_tokenizer,
    llm_api_key,
    llm_provider,
    aws_region_name=None,
    aws_access_key_id=None,
    aws_secret_access_key=None,
    aws_profile_name=None,
):
    """
    Create and return an embedding engine based on the specified provider.

    Parameters:
    -----------

        - embedding_provider: The name of the embedding provider, e.g., 'fastembed',
          'ollama', or another supported provider.
        - embedding_model: The model to be used for the embedding engine.
        - embedding_dimensions: The number of dimensions for the embeddings.
        - embedding_max_completion_tokens: The maximum number of tokens for the embeddings.
        - embedding_endpoint: The endpoint for the embedding service, relevant for certain
          providers.
        - embedding_api_key: API key to authenticate with the embedding service, if
          required.
        - embedding_api_version: Version of the API to be used for the embedding service, if
          applicable.
        - huggingface_tokenizer: Tokenizer from Hugging Face for tokenizing input text, used
          for specific providers.
        - llm_api_key: API key for the LLM service, to be used if embedding_api_key is not
          provided.
        - aws_region_name: AWS region for Bedrock embeddings
        - aws_access_key_id: AWS access key for Bedrock
        - aws_secret_access_key: AWS secret key for Bedrock
        - aws_profile_name: AWS profile name from ~/.aws/credentials

    Returns:
    --------

        Returns an instance of an embedding engine based on the specified provider.
    """
    if embedding_provider == "fastembed":
        from .FastembedEmbeddingEngine import FastembedEmbeddingEngine

        return FastembedEmbeddingEngine(
            model=embedding_model,
            dimensions=embedding_dimensions,
            max_completion_tokens=embedding_max_completion_tokens,
        )

    if embedding_provider == "ollama":
        from .OllamaEmbeddingEngine import OllamaEmbeddingEngine

        return OllamaEmbeddingEngine(
            model=embedding_model,
            dimensions=embedding_dimensions,
            max_completion_tokens=embedding_max_completion_tokens,
            endpoint=embedding_endpoint,
            huggingface_tokenizer=huggingface_tokenizer,
        )

    from .LiteLLMEmbeddingEngine import LiteLLMEmbeddingEngine

    return LiteLLMEmbeddingEngine(
        provider=embedding_provider,
        api_key=embedding_api_key
        or (embedding_api_key if llm_provider == "custom" else llm_api_key),
        endpoint=embedding_endpoint,
        api_version=embedding_api_version,
        model=embedding_model,
        dimensions=embedding_dimensions,
        max_completion_tokens=embedding_max_completion_tokens,
        aws_region_name=aws_region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_profile_name=aws_profile_name,
    )
