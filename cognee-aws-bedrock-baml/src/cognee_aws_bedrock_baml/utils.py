"""Utility functions for AWS Bedrock BAML adapters"""


def ensure_bedrock_prefix(model: str) -> str:
    """
    Ensure model ID has the 'bedrock/' prefix.

    Parameters:
    -----------
        model (str): The model identifier

    Returns:
    --------
        str: Model ID with 'bedrock/' prefix
    """
    return model if model.startswith("bedrock/") else f"bedrock/{model}"


def remove_bedrock_prefix(model: str) -> str:
    """
    Remove 'bedrock/' prefix from model ID if present.

    Parameters:
    -----------
        model (str): The model identifier

    Returns:
    --------
        str: Model ID without 'bedrock/' prefix
    """
    return model[8:] if model.startswith("bedrock/") else model
