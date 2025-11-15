"""Utility functions for GitHub Copilot adapter."""


def ensure_github_copilot_prefix(model: str) -> str:
    """
    Ensure the model identifier has the 'github_copilot/' prefix.
    
    Parameters:
    -----------
        model (str): The model identifier, with or without the prefix.
        
    Returns:
    --------
        str: The model identifier with the 'github_copilot/' prefix.
        
    Example:
    --------
        >>> ensure_github_copilot_prefix("gpt-4o")
        'github_copilot/gpt-4o'
        >>> ensure_github_copilot_prefix("github_copilot/claude-sonnet-3.5")
        'github_copilot/claude-sonnet-3.5'
    """
    if not model.startswith("github_copilot/"):
        return f"github_copilot/{model}"
    return model
