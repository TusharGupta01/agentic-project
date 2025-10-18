#!/usr/bin/env python3
"""
Demo script showing email and text writing capabilities.
"""

from tools.email_writing_tool import (
    write_email,
    write_text_message,
    suggest_email_improvements,
    get_communication_templates
)

def demo_email_writing():
    """Demonstrate email writing capabilities."""
    print("📧 Email Writing Demo")
    print("=" * 50)
    
    # Demo 1: Professional Email
    print("\n📧 Demo 1: Professional Email")
    print("-" * 30)
    result = write_email.invoke({
        "recipient": "john.doe@company.com",
        "subject": "Project Update and Next Steps",
        "body": "I wanted to provide you with an update on our current project status. We have completed the initial phase and are ready to move forward with the next milestone. I would like to schedule a meeting to discuss the timeline and resource allocation.",
        "sender_name": "Jane Smith",
        "email_type": "professional",
        "sender_email": "jane.smith@company.com"
    })
    print(result[:600] + "..." if len(result) > 600 else result)
    
    # Demo 2: Meeting Request Email
    print("\n📅 Demo 2: Meeting Request Email")
    print("-" * 30)
    result = write_email.invoke({
        "recipient": "team@company.com",
        "subject": "Weekly Team Sync Meeting",
        "body": "I would like to schedule our weekly team sync meeting for next week. Please let me know your availability.",
        "sender_name": "Project Manager",
        "email_type": "meeting_request"
    })
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Demo 3: Thank You Email
    print("\n🙏 Demo 3: Thank You Email")
    print("-" * 30)
    result = write_email.invoke({
        "recipient": "client@company.com",
        "subject": "Thank You for Your Business",
        "body": "Thank you for choosing our services. We appreciate your trust in our team and look forward to continuing our partnership.",
        "sender_name": "Service Team",
        "email_type": "thank_you"
    })
    print(result[:500] + "..." if len(result) > 500 else result)

def demo_text_messages():
    """Demonstrate text message writing capabilities."""
    print("\n📱 Text Message Writing Demo")
    print("=" * 50)
    
    # Demo 1: Casual Text
    print("\n💬 Demo 1: Casual Text Message")
    print("-" * 30)
    result = write_text_message.invoke({
        "recipient_name": "Sarah",
        "body": "Hey! Are you free for lunch tomorrow? I found this amazing new restaurant downtown.",
        "sender_name": "Mike",
        "message_type": "casual"
    })
    print(result[:400] + "..." if len(result) > 400 else result)
    
    # Demo 2: Professional Text
    print("\n💼 Demo 2: Professional Text Message")
    print("-" * 30)
    result = write_text_message.invoke({
        "recipient_name": "Dr. Johnson",
        "body": "The meeting has been rescheduled to 3 PM today. Please confirm your attendance.",
        "sender_name": "Admin Assistant",
        "message_type": "professional"
    })
    print(result[:400] + "..." if len(result) > 400 else result)
    
    # Demo 3: Urgent Text
    print("\n🚨 Demo 3: Urgent Text Message")
    print("-" * 30)
    result = write_text_message.invoke({
        "recipient_name": "Emergency Contact",
        "body": "Please call me immediately regarding the server issue.",
        "sender_name": "IT Team",
        "message_type": "urgent",
        "urgency": "urgent"
    })
    print(result[:400] + "..." if len(result) > 400 else result)

def demo_email_improvements():
    """Demonstrate email improvement suggestions."""
    print("\n📝 Email Improvement Demo")
    print("=" * 50)
    
    # Demo with a sample email
    sample_email = """
    Hi John,
    
    I hope you are doing well. I wanted to reach out to you regarding the project we discussed last week. I think we should meet to discuss the details and make sure we are on the same page. Let me know when you are available.
    
    Thanks,
    Jane
    """
    
    print("\n📧 Original Email:")
    print("-" * 20)
    print(sample_email)
    
    print("\n💡 Improvement Suggestions:")
    print("-" * 30)
    result = suggest_email_improvements.invoke({
        "email_content": sample_email,
        "target_audience": "professional"
    })
    print(result[:600] + "..." if len(result) > 600 else result)

def show_usage_examples():
    """Show usage examples for the agent."""
    print("\n💡 Usage Examples for the Agent")
    print("=" * 50)
    
    examples = [
        "Write a professional email to john@company.com about a meeting request",
        "Write a casual text message to my friend about lunch plans",
        "Write a thank you email to a client for their business",
        "Write an urgent text message about a server issue",
        "Help me improve this email draft: 'Hi, meeting tomorrow?'",
        "Show me available email templates",
        "Write a follow-up email about our previous conversation",
        "Write a meeting reminder text message",
        "Write an apology email for the delay",
        "Write a formal email to a government official"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i:2d}. {example}")
    
    print(f"\n🎯 The agent can now help you with:")
    print("   • Professional email writing")
    print("   • Casual and formal text messages")
    print("   • Email improvement suggestions")
    print("   • Communication templates")
    print("   • Meeting requests and follow-ups")
    print("   • Thank you and apology messages")
    print("   • Urgent and informational communications")

def show_available_templates():
    """Show available communication templates."""
    print("\n📋 Available Communication Templates")
    print("=" * 50)
    
    result = get_communication_templates.invoke({
        "template_type": "all"
    })
    print(result[:800] + "..." if len(result) > 800 else result)

if __name__ == "__main__":
    demo_email_writing()
    demo_text_messages()
    demo_email_improvements()
    show_available_templates()
    show_usage_examples()
    
    print(f"\n✅ Email Writing Agent is ready!")
    print(f"🚀 Start the server with: python main.py")
    print(f"🛡️  Or use safe mode: python run_safe.py")
    print(f"\n💬 Example API call:")
    print(f'curl -X POST "http://localhost:8000/api/chat" \\')
    print(f'  -H "Content-Type: application/json" \\')
    print(f'  -d \'{{"message": "Write a professional email to john@company.com about a meeting request"}}\'')
