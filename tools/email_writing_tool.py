"""
Email and text writing tools for the AI agent.
"""

from typing import Dict, Any, Optional, List
from langchain_core.tools import tool
from datetime import datetime
import re


def _validate_email(email: str) -> bool:
    """Basic email validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def _format_recipient_info(recipient: str) -> Dict[str, str]:
    """Parse recipient information."""
    if '<' in recipient and '>' in recipient:
        # Format: "Name <email@domain.com>"
        name_match = re.search(r'^(.+?)\s*<(.+?)>$', recipient.strip())
        if name_match:
            return {"name": name_match.group(1).strip(), "email": name_match.group(2).strip()}
    
    # Check if it's just an email
    if _validate_email(recipient):
        return {"name": "", "email": recipient.strip()}
    
    # Assume it's just a name
    return {"name": recipient.strip(), "email": ""}


def _get_email_templates() -> Dict[str, str]:
    """Get predefined email templates."""
    return {
        "professional": """
Subject: {subject}

Dear {recipient_name},

{body}

Best regards,
{sender_name}
        """.strip(),
        
        "formal": """
Subject: {subject}

Dear {recipient_name},

I hope this email finds you well.

{body}

I look forward to your response.

Sincerely,
{sender_name}
        """.strip(),
        
        "casual": """
Subject: {subject}

Hi {recipient_name},

{body}

Thanks!
{sender_name}
        """.strip(),
        
        "follow_up": """
Subject: Follow-up: {subject}

Dear {recipient_name},

I wanted to follow up on {follow_up_topic}.

{body}

Please let me know if you need any additional information.

Best regards,
{sender_name}
        """.strip(),
        
        "meeting_request": """
Subject: Meeting Request: {subject}

Dear {recipient_name},

I hope you're doing well. I would like to schedule a meeting to discuss {meeting_topic}.

{body}

Please let me know your availability for the following times:
{meeting_times}

Looking forward to hearing from you.

Best regards,
{sender_name}
        """.strip(),
        
        "thank_you": """
Subject: Thank You - {subject}

Dear {recipient_name},

Thank you for {thank_you_reason}.

{body}

I truly appreciate your {appreciation_reason}.

Best regards,
{sender_name}
        """.strip(),
        
        "apology": """
Subject: Apology - {subject}

Dear {recipient_name},

I would like to sincerely apologize for {apology_reason}.

{body}

I understand the inconvenience this may have caused and I am committed to {resolution_plan}.

Sincerely,
{sender_name}
        """.strip()
    }


def _get_text_templates() -> Dict[str, str]:
    """Get predefined text message templates."""
    return {
        "casual": "Hey {recipient_name}! {body} - {sender_name}",
        "professional": "Hello {recipient_name}, {body}. Best regards, {sender_name}",
        "urgent": "Hi {recipient_name}, urgent: {body}. Please respond ASAP. - {sender_name}",
        "informational": "Hi {recipient_name}, just wanted to let you know: {body}. - {sender_name}",
        "meeting_reminder": "Reminder: {body} at {meeting_time}. See you there! - {sender_name}",
        "thank_you": "Thank you {recipient_name} for {thank_you_reason}! {body} - {sender_name}"
    }


@tool
def write_email(
    recipient: str,
    subject: str,
    body: str,
    sender_name: str,
    email_type: str = "professional",
    sender_email: str = "",
    cc: str = "",
    bcc: str = "",
    priority: str = "normal"
) -> str:
    """Write a professional email based on provided details."""
    try:
        # Validate inputs
        if not recipient or not subject or not body or not sender_name:
            return "Error: recipient, subject, body, and sender_name are required fields."
        
        # Parse recipient information
        recipient_info = _format_recipient_info(recipient)
        recipient_name = recipient_info["name"] or recipient_info["email"] or "Sir/Madam"
        
        # Get email templates
        templates = _get_email_templates()
        
        if email_type not in templates:
            available_types = ", ".join(templates.keys())
            return f"Error: Invalid email type '{email_type}'. Available types: {available_types}"
        
        # Select template
        template = templates[email_type]
        
        # Format the email
        email_content = template.format(
            recipient_name=recipient_name,
            subject=subject,
            body=body,
            sender_name=sender_name,
            sender_email=sender_email,
            follow_up_topic=getattr(write_email, 'follow_up_topic', 'our previous conversation'),
            meeting_topic=getattr(write_email, 'meeting_topic', 'the project'),
            meeting_times=getattr(write_email, 'meeting_times', 'next week'),
            thank_you_reason=getattr(write_email, 'thank_you_reason', 'your help'),
            appreciation_reason=getattr(write_email, 'appreciation_reason', 'time and effort'),
            apology_reason=getattr(write_email, 'apology_reason', 'the delay'),
            resolution_plan=getattr(write_email, 'resolution_plan', 'ensuring this doesn\'t happen again')
        )
        
        # Add email headers
        result = f"📧 EMAIL DRAFT\n"
        result += "=" * 50 + "\n\n"
        
        # Email metadata
        result += f"To: {recipient}\n"
        if sender_email:
            result += f"From: {sender_name} <{sender_email}>\n"
        else:
            result += f"From: {sender_name}\n"
        
        if cc:
            result += f"CC: {cc}\n"
        if bcc:
            result += f"BCC: {bcc}\n"
        
        result += f"Priority: {priority.title()}\n"
        result += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Email content
        result += email_content
        
        # Add suggestions
        result += f"\n\n💡 SUGGESTIONS:\n"
        result += f"- Review the content before sending\n"
        result += f"- Check recipient email address: {recipient_info['email'] or 'Not provided'}\n"
        result += f"- Consider adding attachments if needed\n"
        result += f"- Verify the tone matches your intent\n"
        
        return result
        
    except Exception as e:
        return f"Error writing email: {str(e)}"


@tool
def write_text_message(
    recipient_name: str,
    body: str,
    sender_name: str,
    message_type: str = "casual",
    urgency: str = "normal"
) -> str:
    """Write a text message based on provided details."""
    try:
        # Validate inputs
        if not recipient_name or not body or not sender_name:
            return "Error: recipient_name, body, and sender_name are required fields."
        
        # Get text templates
        templates = _get_text_templates()
        
        if message_type not in templates:
            available_types = ", ".join(templates.keys())
            return f"Error: Invalid message type '{message_type}'. Available types: {available_types}"
        
        # Select template
        template = templates[message_type]
        
        # Format the message
        message_content = template.format(
            recipient_name=recipient_name,
            body=body,
            sender_name=sender_name,
            meeting_time=getattr(write_text_message, 'meeting_time', '2:00 PM'),
            thank_you_reason=getattr(write_text_message, 'thank_you_reason', 'your help')
        )
        
        # Add urgency indicator if needed
        if urgency.lower() == "urgent":
            message_content = f"🚨 URGENT: {message_content}"
        
        # Format result
        result = f"📱 TEXT MESSAGE DRAFT\n"
        result += "=" * 50 + "\n\n"
        
        result += f"To: {recipient_name}\n"
        result += f"From: {sender_name}\n"
        result += f"Type: {message_type.title()}\n"
        result += f"Urgency: {urgency.title()}\n"
        result += f"Length: {len(message_content)} characters\n\n"
        
        result += f"Message:\n{message_content}\n\n"
        
        # Add suggestions
        result += f"💡 SUGGESTIONS:\n"
        result += f"- Keep it concise and clear\n"
        result += f"- Check spelling and grammar\n"
        result += f"- Consider the recipient's preferred communication style\n"
        
        if len(message_content) > 160:
            result += f"- Consider splitting into multiple messages (current: {len(message_content)} chars)\n"
        
        return result
        
    except Exception as e:
        return f"Error writing text message: {str(e)}"


@tool
def suggest_email_improvements(email_content: str, target_audience: str = "general") -> str:
    """Suggest improvements for an email draft."""
    try:
        if not email_content:
            return "Error: email_content is required."
        
        result = f"📝 EMAIL IMPROVEMENT SUGGESTIONS\n"
        result += "=" * 50 + "\n\n"
        
        # Basic analysis
        word_count = len(email_content.split())
        char_count = len(email_content)
        sentences = email_content.count('.') + email_content.count('!') + email_content.count('?')
        
        result += f"📊 ANALYSIS:\n"
        result += f"   Word count: {word_count}\n"
        result += f"   Character count: {char_count}\n"
        result += f"   Sentences: {sentences}\n"
        result += f"   Target audience: {target_audience}\n\n"
        
        # Suggestions based on analysis
        suggestions = []
        
        if word_count > 200:
            suggestions.append("Consider shortening the email - aim for 150-200 words for better readability")
        
        if word_count < 50:
            suggestions.append("The email might be too brief - consider adding more context or details")
        
        if sentences > 10:
            suggestions.append("Consider breaking long sentences into shorter ones for clarity")
        
        if not email_content.lower().startswith(('dear', 'hi', 'hello', 'good morning', 'good afternoon')):
            suggestions.append("Consider adding a proper greeting")
        
        if not any(word in email_content.lower() for word in ['sincerely', 'best regards', 'thanks', 'thank you']):
            suggestions.append("Consider adding a proper closing")
        
        # Audience-specific suggestions
        if target_audience.lower() == "professional":
            if any(word in email_content.lower() for word in ['hey', 'hi there', 'what\'s up']):
                suggestions.append("Consider using more formal greetings for professional communication")
        
        if target_audience.lower() == "casual":
            if any(word in email_content.lower() for word in ['sincerely', 'respectfully', 'yours truly']):
                suggestions.append("Consider using more casual closings for informal communication")
        
        # Format suggestions
        if suggestions:
            result += f"💡 SUGGESTIONS:\n"
            for i, suggestion in enumerate(suggestions, 1):
                result += f"   {i}. {suggestion}\n"
        else:
            result += f"✅ The email looks good! No major improvements needed.\n"
        
        result += f"\n📋 GENERAL TIPS:\n"
        result += f"   • Use clear, concise language\n"
        result += f"   • Include a clear subject line\n"
        result += f"   • Proofread for spelling and grammar\n"
        result += f"   • Consider the recipient's perspective\n"
        result += f"   • Use bullet points for multiple items\n"
        
        return result
        
    except Exception as e:
        return f"Error analyzing email: {str(e)}"


@tool
def get_communication_templates(template_type: str = "all") -> str:
    """Get available email and text message templates."""
    try:
        result = f"📋 COMMUNICATION TEMPLATES\n"
        result += "=" * 50 + "\n\n"
        
        if template_type.lower() in ["all", "email"]:
            result += f"📧 EMAIL TEMPLATES:\n"
            email_templates = _get_email_templates()
            for template_name, template_content in email_templates.items():
                result += f"   • {template_name.title()}: {template_content.split('Subject:')[0].strip()}\n"
            result += "\n"
        
        if template_type.lower() in ["all", "text"]:
            result += f"📱 TEXT MESSAGE TEMPLATES:\n"
            text_templates = _get_text_templates()
            for template_name, template_content in text_templates.items():
                result += f"   • {template_name.title()}: {template_content}\n"
            result += "\n"
        
        result += f"💡 USAGE EXAMPLES:\n"
        result += f"   • write_email(recipient='john@example.com', subject='Meeting Request', body='...', sender_name='Jane')\n"
        result += f"   • write_text_message(recipient_name='John', body='...', sender_name='Jane')\n"
        result += f"   • suggest_email_improvements(email_content='...', target_audience='professional')\n"
        
        return result
        
    except Exception as e:
        return f"Error getting templates: {str(e)}"
