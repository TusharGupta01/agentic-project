from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from agent import run_agent
from agent.model_config import ModelConfig, estimate_cost

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
        "agent_name": "Browsing History Analysis Agent",
        "description": "Specialized AI agent for analyzing and understanding your browsing history",
        "capabilities": [
            "Chrome browser history analysis",
            "Browsing pattern insights",
            "Domain visit statistics",
            "Search through browsing history",
            "Weather information (mock)",
            "Knowledge search (mock)",
            "General conversation"
        ],
        "tools": [
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
