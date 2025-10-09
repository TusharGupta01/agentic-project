"""
Language model configuration and initialization.
"""

from .model_config import get_llm as get_configured_llm


def get_llm():
    """Initialize the language model with the cheapest available option."""
    # Use the cheapest model by default
    return get_configured_llm("cheapest")
