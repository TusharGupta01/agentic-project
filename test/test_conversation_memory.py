#!/usr/bin/env python3
"""
Test script for conversation memory functionality.
"""

import sys
sys.path.append('..')
from agent.memory import conversation_memory
from agent.workflow import run_agent
from agent.lcel_agent import run_lcel_agent
from langchain_core.messages import HumanMessage, AIMessage

def test_memory_basic():
    """Test basic memory functionality."""
    print("🧠 Testing Basic Memory Functionality")
    print("=" * 40)
    
    # Create a session
    session_id = conversation_memory.create_session()
    print(f"Created session: {session_id}")
    
    # Add some messages
    conversation_memory.add_message(session_id, HumanMessage(content="Hello"))
    conversation_memory.add_message(session_id, AIMessage(content="Hi there!"))
    conversation_memory.add_message(session_id, HumanMessage(content="How are you?"))
    conversation_memory.add_message(session_id, AIMessage(content="I'm doing well, thanks!"))
    
    # Get messages
    messages = conversation_memory.get_messages(session_id)
    print(f"Total messages: {len(messages)}")
    
    for i, msg in enumerate(messages):
        print(f"  {i+1}. {type(msg).__name__}: {msg.content}")
    
    # Get session info
    info = conversation_memory.get_session_info(session_id)
    print(f"\nSession info: {info}")

def test_langgraph_memory():
    """Test LangGraph agent with memory."""
    print("\n🔄 Testing LangGraph Agent with Memory")
    print("=" * 40)
    
    # Create a session
    session_id = conversation_memory.create_session()
    print(f"Created session: {session_id}")
    
    # Test conversation flow
    queries = [
        "Hello, my name is John",
        "What's my name?",
        "Show me my recent browsing history",
        "What did I just ask you about?"
    ]
    
    for query in queries:
        print(f"\nUser: {query}")
        try:
            response = run_agent(query, session_id)
            print(f"Agent: {response[:150]}...")
        except Exception as e:
            print(f"Error: {e}")

def test_lcel_memory():
    """Test LCEL agent with memory."""
    print("\n🔗 Testing LCEL Agent with Memory")
    print("=" * 40)
    
    # Create a session
    session_id = conversation_memory.create_session()
    print(f"Created session: {session_id}")
    
    # Test conversation flow
    queries = [
        "Hello, I'm interested in Python programming",
        "What programming language am I interested in?",
        "Show me my recent browsing history",
        "What was my first message about?"
    ]
    
    for query in queries:
        print(f"\nUser: {query}")
        try:
            response = run_lcel_agent(query, session_id)
            print(f"Agent: {response[:150]}...")
        except Exception as e:
            print(f"Error: {e}")

def test_session_management():
    """Test session management features."""
    print("\n📋 Testing Session Management")
    print("=" * 40)
    
    # Create multiple sessions
    session1 = conversation_memory.create_session()
    session2 = conversation_memory.create_session()
    
    # Add messages to both sessions
    conversation_memory.add_message(session1, HumanMessage(content="Session 1 message"))
    conversation_memory.add_message(session2, HumanMessage(content="Session 2 message"))
    
    # List all sessions
    all_sessions = conversation_memory.get_all_sessions()
    print(f"Total sessions: {len(all_sessions)}")
    
    for session in all_sessions:
        print(f"  Session: {session['session_id'][:8]}... - {session['message_count']} messages")
    
    # Clear one session
    conversation_memory.clear_session(session1)
    info1 = conversation_memory.get_session_info(session1)
    info2 = conversation_memory.get_session_info(session2)
    
    print(f"\nAfter clearing session 1:")
    print(f"  Session 1 messages: {info1['message_count']}")
    print(f"  Session 2 messages: {info2['message_count']}")
    
    # Delete a session
    conversation_memory.delete_session(session1)
    remaining_sessions = conversation_memory.get_all_sessions()
    print(f"\nAfter deleting session 1: {len(remaining_sessions)} sessions remaining")

def test_memory_persistence():
    """Test that memory persists across multiple calls."""
    print("\n💾 Testing Memory Persistence")
    print("=" * 40)
    
    # Create a session
    session_id = conversation_memory.create_session()
    
    # First conversation
    print("First conversation:")
    response1 = run_agent("My favorite color is blue", session_id)
    print(f"Agent: {response1[:100]}...")
    
    # Second conversation (should remember the color)
    print("\nSecond conversation:")
    response2 = run_agent("What's my favorite color?", session_id)
    print(f"Agent: {response2[:100]}...")
    
    # Third conversation (should still remember)
    print("\nThird conversation:")
    response3 = run_agent("Can you remind me what I told you about my preferences?", session_id)
    print(f"Agent: {response3[:100]}...")

def compare_agents_memory():
    """Compare how both agents handle memory."""
    print("\n⚖️ Comparing Agent Memory Handling")
    print("=" * 50)
    
    # Test with LangGraph
    print("🔄 LangGraph Agent:")
    session1 = conversation_memory.create_session()
    queries = ["I love pizza", "What food do I love?"]
    
    for query in queries:
        print(f"  User: {query}")
        response = run_agent(query, session1)
        print(f"  Agent: {response[:80]}...")
    
    # Test with LCEL
    print("\n🔗 LCEL Agent:")
    session2 = conversation_memory.create_session()
    
    for query in queries:
        print(f"  User: {query}")
        response = run_lcel_agent(query, session2)
        print(f"  Agent: {response[:80]}...")

if __name__ == "__main__":
    print("🧠 Conversation Memory Test Suite")
    print("=" * 50)
    
    try:
        test_memory_basic()
        test_langgraph_memory()
        test_lcel_memory()
        test_session_management()
        test_memory_persistence()
        compare_agents_memory()
        
        print("\n✅ All memory tests completed!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
