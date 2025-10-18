#!/usr/bin/env python3
"""
Test script for email writing functionality.
"""

import sys
sys.path.append('..')
from tools.email_writing_tool import (
    write_email,
    write_text_message,
    suggest_email_improvements,
    get_communication_templates
)

def test_write_email():
    """Test email writing functionality."""
    print("📧 Testing write_email")
    print("=" * 40)
    
    # Test professional email
    result = write_email.invoke({
        "recipient": "john.doe@company.com",
        "subject": "Meeting Request for Project Discussion",
        "body": "I would like to schedule a meeting to discuss the upcoming project timeline and deliverables. Please let me know your availability for next week.",
        "sender_name": "Jane Smith",
        "email_type": "professional",
        "sender_email": "jane.smith@company.com"
    })
    print(result[:500] + "..." if len(result) > 500 else result)

def test_write_text_message():
    """Test text message writing functionality."""
    print("\n📱 Testing write_text_message")
    print("=" * 40)
    
    # Test casual text message
    result = write_text_message.invoke({
        "recipient_name": "John",
        "body": "Hey! Just wanted to remind you about our meeting tomorrow at 2 PM. See you there!",
        "sender_name": "Jane",
        "message_type": "casual"
    })
    print(result[:400] + "..." if len(result) > 400 else result)

def test_suggest_improvements():
    """Test email improvement suggestions."""
    print("\n📝 Testing suggest_email_improvements")
    print("=" * 40)
    
    # Test with a sample email
    sample_email = """
    Hi John,
    
    I hope you are doing well. I wanted to reach out to you regarding the project we discussed last week. I think we should meet to discuss the details and make sure we are on the same page. Let me know when you are available.
    
    Thanks,
    Jane
    """
    
    result = suggest_email_improvements.invoke({
        "email_content": sample_email,
        "target_audience": "professional"
    })
    print(result[:400] + "..." if len(result) > 400 else result)

def test_get_templates():
    """Test getting communication templates."""
    print("\n📋 Testing get_communication_templates")
    print("=" * 40)
    
    result = get_communication_templates.invoke({
        "template_type": "all"
    })
    print(result[:400] + "..." if len(result) > 400 else result)

def test_different_email_types():
    """Test different email types."""
    print("\n🎭 Testing Different Email Types")
    print("=" * 40)
    
    email_types = ["professional", "formal", "casual", "follow_up", "meeting_request", "thank_you", "apology"]
    
    for email_type in email_types:
        print(f"\n--- {email_type.upper()} EMAIL ---")
        result = write_email.invoke({
            "recipient": "colleague@company.com",
            "subject": f"Sample {email_type.title()} Email",
            "body": f"This is a sample {email_type} email to demonstrate the template.",
            "sender_name": "Jane Smith",
            "email_type": email_type
        })
        print(result[:200] + "..." if len(result) > 200 else result)

def test_different_text_types():
    """Test different text message types."""
    print("\n💬 Testing Different Text Message Types")
    print("=" * 40)
    
    text_types = ["casual", "professional", "urgent", "informational", "meeting_reminder", "thank_you"]
    
    for text_type in text_types:
        print(f"\n--- {text_type.upper()} TEXT ---")
        result = write_text_message.invoke({
            "recipient_name": "John",
            "body": f"This is a sample {text_type} text message.",
            "sender_name": "Jane",
            "message_type": text_type
        })
        print(result[:150] + "..." if len(result) > 150 else result)

def test_agent_integration():
    """Test the agent with email writing."""
    print("\n🤖 Testing Agent Integration")
    print("=" * 40)
    
    from agent.workflow import run_agent
    from agent.memory import conversation_memory
    
    # Create a session
    session_id = conversation_memory.create_session()
    
    # Test queries
    queries = [
        "Write a professional email to john@company.com about a meeting request",
        "Write a casual text message to my friend about lunch plans",
        "Show me available email templates",
        "Help me improve this email draft: 'Hi, meeting tomorrow?'"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        try:
            result = run_agent(query, session_id)
            print(f"Response: {result[:200]}...")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("🧪 Email Writing Test Suite")
    print("=" * 50)
    
    try:
        test_write_email()
        test_write_text_message()
        test_suggest_improvements()
        test_get_templates()
        test_different_email_types()
        test_different_text_types()
        test_agent_integration()
        
        print("\n✅ All email writing tests completed!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
