"""Utility functions for AWS Bedrock adapters"""


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
