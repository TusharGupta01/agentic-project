"""
Language model configuration and initialization.
"""

import os
from langchain_openai import ChatOpenAI


def get_llm():
    """Initialize the language model."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        api_key=api_key
    )
