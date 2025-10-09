"""
Model configuration options for different cost levels.
"""

import os
from langchain_openai import ChatOpenAI
from typing import Optional


class ModelConfig:
    """Configuration for different OpenAI models and cost levels."""
    
    # Model configurations with cost information
    MODELS = {
        "cheapest": {
            "model": "gpt-3.5-turbo-1106",
            "temperature": 0.3,
            "max_tokens": 1000,
            "cost_per_1k_input": 0.001,
            "cost_per_1k_output": 0.002,
            "description": "Cheapest option - Good for simple tasks"
        },
        "balanced": {
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 2000,
            "cost_per_1k_input": 0.0015,
            "cost_per_1k_output": 0.002,
            "description": "Balanced cost and performance"
        },
        "premium": {
            "model": "gpt-4-turbo-preview",
            "temperature": 0.7,
            "max_tokens": 4000,
            "cost_per_1k_input": 0.01,
            "cost_per_1k_output": 0.03,
            "description": "Highest quality - Most expensive"
        }
    }
    
    @classmethod
    def get_llm(cls, model_tier: str = "cheapest") -> ChatOpenAI:
        """Get LLM configured for the specified cost tier."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        if model_tier not in cls.MODELS:
            raise ValueError(f"Invalid model tier: {model_tier}. Available: {list(cls.MODELS.keys())}")
        
        config = cls.MODELS[model_tier]
        
        return ChatOpenAI(
            model=config["model"],
            temperature=config["temperature"],
            max_tokens=config["max_tokens"],
            api_key=api_key
        )
    
    @classmethod
    def get_model_info(cls, model_tier: str = "cheapest") -> dict:
        """Get information about a specific model tier."""
        if model_tier not in cls.MODELS:
            raise ValueError(f"Invalid model tier: {model_tier}. Available: {list(cls.MODELS.keys())}")
        
        return cls.MODELS[model_tier]
    
    @classmethod
    def list_models(cls) -> dict:
        """List all available model configurations."""
        return cls.MODELS


def get_llm(model_tier: str = "cheapest") -> ChatOpenAI:
    """Convenience function to get LLM with specified tier."""
    return ModelConfig.get_llm(model_tier)


def estimate_cost(input_tokens: int, output_tokens: int, model_tier: str = "cheapest") -> float:
    """Estimate the cost for a given number of tokens."""
    config = ModelConfig.get_model_info(model_tier)
    
    input_cost = (input_tokens / 1000) * config["cost_per_1k_input"]
    output_cost = (output_tokens / 1000) * config["cost_per_1k_output"]
    
    return input_cost + output_cost
