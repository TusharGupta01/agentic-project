#!/usr/bin/env python3
"""
Test script for model configuration and cost estimation.
"""

from agent.model_config import ModelConfig, estimate_cost
import sys
sys.path.append('..')

def test_model_config():
    """Test the model configuration system."""
    print("🤖 Model Configuration Test")
    print("=" * 50)
    
    # List all available models
    print("\n📋 Available Models:")
    models = ModelConfig.list_models()
    for tier, config in models.items():
        print(f"\n{tier.upper()}:")
        print(f"  Model: {config['model']}")
        print(f"  Cost: ${config['cost_per_1k_input']}/1K input, ${config['cost_per_1k_output']}/1K output")
        print(f"  Description: {config['description']}")
    
    # Test cost estimation
    print("\n💰 Cost Estimation Examples:")
    print("=" * 30)
    
    examples = [
        (1000, 500, "Simple query"),
        (2000, 1000, "Complex analysis"),
        (5000, 2000, "Long conversation")
    ]
    
    for input_tokens, output_tokens, description in examples:
        print(f"\n{description} ({input_tokens} input, {output_tokens} output tokens):")
        for tier in ["cheapest", "balanced", "premium"]:
            cost = estimate_cost(input_tokens, output_tokens, tier)
            print(f"  {tier}: ${cost:.4f}")
    
    # Show current configuration
    print("\n⚙️  Current Configuration:")
    current = ModelConfig.get_model_info("cheapest")
    print(f"  Model: {current['model']}")
    print(f"  Temperature: {current['temperature']}")
    print(f"  Max Tokens: {current['max_tokens']}")
    print(f"  Cost: ${current['cost_per_1k_input']}/1K input, ${current['cost_per_1k_output']}/1K output")

def show_cost_savings():
    """Show potential cost savings with the cheapest model."""
    print("\n💡 Cost Savings with Cheapest Model:")
    print("=" * 40)
    
    # Compare costs for different usage scenarios
    scenarios = [
        (1000, 500, "Daily usage (10 queries)"),
        (5000, 2000, "Heavy usage (5 queries)"),
        (10000, 5000, "Very heavy usage (2 queries)")
    ]
    
    for input_tokens, output_tokens, scenario in scenarios:
        cheapest_cost = estimate_cost(input_tokens, output_tokens, "cheapest")
        premium_cost = estimate_cost(input_tokens, output_tokens, "premium")
        savings = premium_cost - cheapest_cost
        savings_percent = (savings / premium_cost) * 100 if premium_cost > 0 else 0
        
        print(f"\n{scenario}:")
        print(f"  Cheapest: ${cheapest_cost:.4f}")
        print(f"  Premium:  ${premium_cost:.4f}")
        print(f"  Savings:  ${savings:.4f} ({savings_percent:.1f}%)")

if __name__ == "__main__":
    test_model_config()
    show_cost_savings()
    
    print("\n✅ Model configuration test completed!")
    print("\nYour agent is now configured to use the cheapest available model.")
    print("This will significantly reduce your API costs while maintaining good performance.")
