#!/usr/bin/env python3
"""
Test script for the AI Agent without requiring OpenAI API key.
This demonstrates the agent structure and tool functionality.
"""

import os
import sys
sys.path.append('..')
from tools import get_weather, search_knowledge

def test_tools():
    """Test the individual tools without the LLM."""
    print("🧪 Testing AI Agent Tools")
    print("=" * 50)
    
    # Test weather tool
    print("\n🌤️  Testing Weather Tool:")
    weather_tests = ["Tokyo", "New York", "London", "Unknown City"]
    
    for city in weather_tests:
        result = get_weather.invoke({"city": city})
        print(f"  {city}: {result}")
    
    # Test knowledge search tool
    print("\n📚 Testing Knowledge Search Tool:")
    knowledge_tests = ["python", "fastapi", "langgraph", "unknown topic"]
    
    for topic in knowledge_tests:
        result = search_knowledge.invoke({"query": topic})
        print(f"  {topic}: {result}")

def test_agent_structure():
    """Test the agent structure without running the LLM."""
    print("\n🏗️  Testing Agent Structure")
    print("=" * 50)
    
    try:
        from agent import create_agent_graph, AgentState
        
        # Create the agent graph
        agent_app = create_agent_graph()
        print("✅ Agent graph created successfully")
        
        # Test state structure
        test_state = AgentState(
            messages=[],
            user_input="test",
            final_response=""
        )
        print("✅ Agent state structure is valid")
        
        print(f"✅ Agent has {len(agent_app.nodes)} nodes")
        
    except Exception as e:
        print(f"❌ Error testing agent structure: {e}")

def show_setup_instructions():
    """Show setup instructions for using the agent with OpenAI."""
    print("\n🔧 Setup Instructions")
    print("=" * 50)
    print("To use the AI agent with OpenAI:")
    print("1. Get an OpenAI API key from: https://platform.openai.com/api-keys")
    print("2. Copy env.example to .env:")
    print("   cp env.example .env")
    print("3. Edit .env and add your API key:")
    print("   OPENAI_API_KEY=your_actual_api_key_here")
    print("4. Restart the server:")
    print("   make dev")
    print("5. Test the agent:")
    print('   curl -X POST "http://localhost:8000/api/chat" \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"message": "Show me my recent browsing history"}\'')

if __name__ == "__main__":
    print("🤖 AI Agent Test Suite")
    print("=" * 50)
    
    test_tools()
    test_agent_structure()
    show_setup_instructions()
    
    print("\n✅ All tests completed!")
    print("\nThe AI agent is ready to use once you add your OpenAI API key.")
    print("The agent now specializes in browsing history analysis.")