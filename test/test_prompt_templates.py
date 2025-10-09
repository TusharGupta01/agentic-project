#!/usr/bin/env python3
"""
Test script for ChatPromptTemplate usage.
"""

import sys
sys.path.append('..')
from agent.prompts import (
    get_browsing_history_prompt,
    get_tool_selection_prompt,
    get_response_synthesis_prompt,
    get_conversation_prompt
)

def test_prompt_templates():
    """Test the prompt template system."""
    print("🎯 Testing ChatPromptTemplate System")
    print("=" * 50)
    
    # Test 1: Browsing history prompt
    print("\n📋 Test 1: Browsing History Prompt")
    prompt = get_browsing_history_prompt()
    formatted = prompt.format_messages(user_input="Show me my recent browsing history")
    print(f"System message length: {len(formatted[0].content)} characters")
    print(f"Human message: {formatted[1].content}")
    
    # Test 2: Tool selection prompt
    print("\n🔧 Test 2: Tool Selection Prompt")
    prompt = get_tool_selection_prompt()
    formatted = prompt.format_messages(user_input="What are my most visited websites?")
    print(f"System message length: {len(formatted[0].content)} characters")
    print(f"Human message: {formatted[1].content}")
    
    # Test 3: Response synthesis prompt
    print("\n🔄 Test 3: Response Synthesis Prompt")
    prompt = get_response_synthesis_prompt()
    formatted = prompt.format_messages(
        user_input="Show me my recent browsing history",
        tool_results="Tool: read_chrome_history - Found 5 recent entries"
    )
    print(f"System message length: {len(formatted[0].content)} characters")
    print(f"Human message preview: {formatted[1].content[:100]}...")
    
    # Test 4: Conversation prompt
    print("\n💬 Test 4: Conversation Prompt")
    prompt = get_conversation_prompt()
    formatted = prompt.format_messages(user_input="Hello, how are you?")
    print(f"System message length: {len(formatted[0].content)} characters")
    print(f"Human message: {formatted[1].content}")

def show_prompt_benefits():
    """Show the benefits of using ChatPromptTemplate."""
    print("\n✨ Benefits of ChatPromptTemplate")
    print("=" * 40)
    
    benefits = [
        "🎯 **Structured Prompts** - Clear separation of system and human messages",
        "🔧 **Reusability** - Templates can be reused across different contexts",
        "📝 **Maintainability** - Easy to update prompts without changing code",
        "🧪 **Testability** - Can test prompts independently",
        "📊 **Consistency** - Ensures consistent prompt structure",
        "🔄 **Flexibility** - Easy to add variables and dynamic content",
        "📈 **Scalability** - Can create complex prompt chains",
        "🎨 **Customization** - Easy to create different prompt variants"
    ]
    
    for benefit in benefits:
        print(f"  {benefit}")
    
    print("\n🔍 **Before vs After:**")
    print("  Before: Hardcoded system messages in workflow")
    print("  After: Structured, reusable prompt templates")
    
    print("\n🚀 **Future Possibilities:**")
    print("  - Dynamic prompt selection based on context")
    print("  - A/B testing different prompt versions")
    print("  - User-specific prompt customization")
    print("  - Multi-language prompt support")
    print("  - Prompt versioning and rollback")

def demonstrate_prompt_flexibility():
    """Demonstrate the flexibility of prompt templates."""
    print("\n🎨 Prompt Template Flexibility Demo")
    print("=" * 40)
    
    # Show how we can easily create variations
    base_prompt = get_browsing_history_prompt()
    
    test_queries = [
        "Show me my recent browsing history",
        "What are my most visited websites?",
        "Find websites about machine learning",
        "Analyze my browsing patterns for the last week"
    ]
    
    print("Same prompt template, different queries:")
    for i, query in enumerate(test_queries, 1):
        formatted = base_prompt.format_messages(user_input=query)
        print(f"  {i}. {query}")
        print(f"     → System: {len(formatted[0].content)} chars, Human: {formatted[1].content}")

if __name__ == "__main__":
    test_prompt_templates()
    show_prompt_benefits()
    demonstrate_prompt_flexibility()
    
    print("\n✅ ChatPromptTemplate testing completed!")
    print("\nYour agent now uses structured, maintainable prompt templates!")
    print("This makes the system more professional and easier to extend.")
