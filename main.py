from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from agent import run_agent

# Create FastAPI instance
app = FastAPI(
    title="AI Agent FastAPI Project",
    description="A FastAPI application with AI agent powered by LangGraph",
    version="1.0.0"
)

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    status: str

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
    """Chat with the AI agent powered by LangGraph."""
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        response = run_agent(request.message)
        
        return ChatResponse(
            response=response,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

@app.get("/api/agent/info")
async def agent_info():
    """Get information about the AI agent capabilities."""
    return {
        "agent_name": "LangGraph AI Agent",
        "capabilities": [
            "Mathematical calculations",
            "Weather information (mock)",
            "Knowledge search (mock)",
            "Chrome browser history reading",
            "General conversation"
        ],
        "tools": [
            "calculate - Perform mathematical calculations",
            "get_weather - Get weather information for cities",
            "search_knowledge - Search through knowledge base",
            "read_chrome_history - Read and search Google Chrome browser history"
        ],
        "model": "gpt-3.5-turbo"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
