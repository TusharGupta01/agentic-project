#!/usr/bin/env python3
"""
Run the agent in demo mode (no API keys required).
This mode uses mock responses for demonstration purposes.
"""

import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
from agent.memory import conversation_memory

# Set environment variable for mock data
os.environ["USE_MOCK_CHROME_DATA"] = "true"

# Create FastAPI instance
app = FastAPI(
    title="AI Agent Demo Mode",
    description="A FastAPI application with AI agent in demo mode (no API keys required)",
    version="1.0.0"
)

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    status: str
    session_id: str

class SessionInfo(BaseModel):
    session_id: str
    message_count: int
    created_at: str
    last_accessed: str

def get_demo_response(user_input: str) -> str:
    """Generate a demo response based on user input."""
    user_lower = user_input.lower()
    
    # Email writing responses
    if any(keyword in user_lower for keyword in ["email", "write email", "send email"]):
        return """📧 EMAIL DRAFT (Demo Mode)
==================================================

To: john@company.com
From: Your Name
Priority: Normal
Date: 2025-10-18 15:00:00

Subject: Meeting Request

Dear John,

I would like to schedule a meeting to discuss the project details. Please let me know your availability for next week.

Best regards,
Your Name

💡 SUGGESTIONS:
- Review the content before sending
- Check recipient email address
- Consider adding attachments if needed
- Verify the tone matches your intent

Note: This is a demo response. In full mode, the agent would use AI to generate personalized content."""
    
    # Text message responses
    elif any(keyword in user_lower for keyword in ["text", "message", "sms"]):
        return """📱 TEXT MESSAGE DRAFT (Demo Mode)
==================================================

To: Friend
From: You
Type: Casual
Urgency: Normal
Length: 45 characters

Message:
Hey! Are you free for lunch tomorrow? - You

💡 SUGGESTIONS:
- Keep it concise and clear
- Check spelling and grammar
- Consider the recipient's preferred communication style

Note: This is a demo response. In full mode, the agent would use AI to generate personalized content."""
    
    # File analysis responses
    elif any(keyword in user_lower for keyword in ["file", "folder", "directory", "list", "read"]):
        return """📁 FILE ANALYSIS (Demo Mode)
==================================================

📊 Folder Contents: /demo/path
============================================================

📋 Contents (5 items):

📁 documents
📁 images  
📁 projects
📄 README.md (.md) - 2.1 KB
📄 config.json (.json) - 512 B

💡 SUGGESTIONS:
- Use specific file paths for real analysis
- Consider file permissions
- Check file sizes before processing

Note: This is a demo response. In full mode, the agent would analyze actual files and folders."""
    
    # Chrome history responses
    elif any(keyword in user_lower for keyword in ["history", "browsing", "chrome"]):
        return """🌐 BROWSING HISTORY (Demo Mode)
==================================================

Found 5 history entries:

1. GitHub - https://github.com
2. Stack Overflow - https://stackoverflow.com
3. Python Documentation - https://docs.python.org
4. OpenAI API - https://platform.openai.com
5. FastAPI Documentation - https://fastapi.tiangolo.com

💡 SUGGESTIONS:
- Use real Chrome history for actual data
- Consider privacy implications
- Check browser permissions

Note: This is a demo response. In full mode, the agent would access your actual browsing history."""
    
    # Template responses
    elif any(keyword in user_lower for keyword in ["template", "show templates", "available"]):
        return """📋 COMMUNICATION TEMPLATES (Demo Mode)
==================================================

📧 EMAIL TEMPLATES:
   • Professional: Business communications
   • Formal: Official correspondence
   • Casual: Friendly, informal emails
   • Follow-up: Following up on conversations
   • Meeting Request: Scheduling meetings
   • Thank You: Expressing gratitude
   • Apology: Sincere apologies

📱 TEXT MESSAGE TEMPLATES:
   • Casual: Hey {name}! {message} - {sender}
   • Professional: Hello {name}, {message}. Best regards, {sender}
   • Urgent: Hi {name}, urgent: {message}. Please respond ASAP. - {sender}
   • Informational: Hi {name}, just wanted to let you know: {message}. - {sender}
   • Meeting Reminder: Reminder: {message} at {time}. See you there! - {sender}
   • Thank You: Thank you {name} for {reason}! {message} - {sender}

Note: This is a demo response. In full mode, the agent would show actual template content."""
    
    # Default response
    else:
        return f"""🤖 DEMO MODE RESPONSE
==================================================

You asked: "{user_input}"

I'm running in demo mode, which means I can show you what the agent can do without requiring an OpenAI API key.

🎯 Available Capabilities:
   • Email and text message writing
   • File and folder analysis
   • Chrome browsing history analysis
   • Communication templates
   • Weather information
   • General conversation

💡 To get full AI-powered responses:
   1. Get an OpenAI API key from https://platform.openai.com
   2. Add it to your .env file: OPENAI_API_KEY=your_key_here
   3. Restart the server with: python main.py

🛡️ Current Mode: Demo (no API key required)
🚀 Full Mode: Requires OpenAI API key for AI responses"""

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to AI Agent Demo Mode!", "status": "running", "mode": "demo"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "FastAPI", "mode": "demo"}

# AI Agent endpoints
@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """Chat with the AI agent in demo mode."""
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Create or get session
        if not request.session_id:
            session_id = conversation_memory.create_session()
        else:
            session_id = request.session_id
        
        # Generate demo response
        response = get_demo_response(request.message)
        
        return ChatResponse(
            response=response,
            status="success",
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo mode error: {str(e)}")

@app.get("/api/agent/info")
async def agent_info():
    """Get information about the AI agent capabilities."""
    return {
        "agent_name": "AI Agent Demo Mode",
        "description": "Demo mode - no API keys required",
        "mode": "demo",
        "capabilities": [
            "Email and text message writing (demo)",
            "File and folder analysis (demo)",
            "Chrome browsing history analysis (demo)",
            "Communication templates (demo)",
            "Weather information (demo)",
            "General conversation (demo)"
        ],
        "note": "This is demo mode. For full AI capabilities, add your OpenAI API key to .env file"
    }

# Session management endpoints
@app.post("/api/sessions/new")
async def create_new_session():
    """Create a new conversation session."""
    session_id = conversation_memory.create_session()
    return {"session_id": session_id, "status": "created", "mode": "demo"}

@app.get("/api/sessions/{session_id}", response_model=SessionInfo)
async def get_session_info(session_id: str):
    """Get information about a specific session."""
    session_info = conversation_memory.get_session_info(session_id)
    if not session_info:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionInfo(**session_info)

@app.get("/api/sessions")
async def list_sessions():
    """List all active conversation sessions."""
    return {"sessions": conversation_memory.get_all_sessions(), "mode": "demo"}

if __name__ == "__main__":
    print("🛡️  Running in DEMO MODE (no API keys required)")
    print("   - No OpenAI API key needed")
    print("   - Mock responses for all queries")
    print("   - Full functionality demonstration")
    print("   - Server starting on http://localhost:8000")
    print()
    
    uvicorn.run("run_demo_mode:app", host="0.0.0.0", port=8000, reload=True)
