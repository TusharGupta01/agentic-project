from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
from agent import run_agent
from agent.model_config import ModelConfig, estimate_cost
from agent.memory import conversation_memory

# Create FastAPI instance
app = FastAPI(
    title="AI Agent FastAPI Project",
    description="A FastAPI application with AI agent powered by LangGraph",
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

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI!", "status": "running"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "FastAPI"}

# Example API endpoint
@app.get("/api/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello, {name}!", "greeting": "Welcome to our API"}

# Example POST endpoint
@app.post("/api/echo")
async def echo_data(data: dict):
    return {"received": data, "echo": "Data received successfully"}

# AI Agent endpoints
@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """Chat with the AI agent powered by LangGraph with conversation memory."""
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        response = run_agent(request.message, request.session_id)
        
        # Get the session ID that was used (either provided or newly created)
        if request.session_id:
            session_id = request.session_id
        else:
            # Get the most recently created session
            session_ids = list(conversation_memory.sessions.keys())
            session_id = session_ids[-1] if session_ids else None
        
        return ChatResponse(
            response=response,
            status="success",
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

@app.get("/api/agent/info")
async def agent_info():
    """Get information about the AI agent capabilities."""
    return {
        "agent_name": "File and Folder Analysis Agent",
        "description": "Comprehensive AI agent for analyzing files, folders, and browsing history",
        "capabilities": [
            "File and folder analysis",
            "File content reading and summarization",
            "Folder structure analysis",
            "Text search within files",
            "Chrome browser history analysis",
            "Browsing pattern insights",
            "Domain visit statistics",
            "Search through browsing history",
            "Weather information (mock)",
            "Knowledge search (mock)",
            "General conversation"
        ],
        "tools": [
            "list_folder_contents - List all files and folders in a directory with detailed information",
            "read_file_content - Read and display the content of text files",
            "analyze_folder_structure - Get comprehensive statistics about a folder",
            "search_files_in_folder - Search for text within files in a folder",
            "get_file_summary - Get detailed information about a specific file",
            "read_chrome_history - Read and analyze Google Chrome browser history with multiple analysis types",
            "analyze_browsing_patterns - Analyze browsing patterns and provide insights about web usage",
            "get_weather - Get weather information for cities",
            "search_knowledge - Search through knowledge base"
        ],
        "history_analysis_types": [
            "recent - Get recent browsing history",
            "frequent - Find most frequently visited sites", 
            "domains - Analyze top domains by visit count",
            "search - Search for specific terms in history"
        ],
        "model": "gpt-3.5-turbo-1106 (cheapest)",
        "current_model_tier": "cheapest"
    }

@app.get("/api/model/info")
async def model_info():
    """Get information about available models and current configuration."""
    return {
        "current_model": ModelConfig.get_model_info("cheapest"),
        "available_models": ModelConfig.list_models(),
        "cost_estimation": {
            "example_1000_input_500_output": estimate_cost(1000, 500, "cheapest"),
            "example_2000_input_1000_output": estimate_cost(2000, 1000, "cheapest")
        }
    }

# Session management endpoints
@app.post("/api/sessions/new")
async def create_new_session():
    """Create a new conversation session."""
    session_id = conversation_memory.create_session()
    return {"session_id": session_id, "status": "created"}

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
    return {"sessions": conversation_memory.get_all_sessions()}

@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a conversation session."""
    if session_id not in conversation_memory.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    conversation_memory.delete_session(session_id)
    return {"status": "deleted", "session_id": session_id}

@app.post("/api/sessions/{session_id}/clear")
async def clear_session(session_id: str):
    """Clear all messages from a session."""
    if session_id not in conversation_memory.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    conversation_memory.clear_session(session_id)
    return {"status": "cleared", "session_id": session_id}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
