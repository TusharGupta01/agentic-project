# AI Agent FastAPI Project

A FastAPI application with an AI agent powered by LangGraph, featuring automatic documentation and intelligent conversation capabilities.

## Features

- FastAPI web framework
- AI Agent powered by LangGraph and OpenAI
- Automatic API documentation (Swagger UI)
- Intelligent conversation capabilities
- Tool usage (calculations, weather, knowledge search)
- Health check endpoint
- Hot reload for development

## Setup

### Option 1: Using Makefile (Recommended)
```bash
# Setup virtual environment and install dependencies
make setup

# Run the server
make run

# Or run in development mode with auto-reload
make dev
```

### Option 2: Manual Setup
1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Makefile Commands

Run `make help` to see all available commands:

- `make setup` - Create virtual environment and install dependencies
- `make run` - Run the FastAPI server
- `make dev` - Run server in development mode with auto-reload
- `make prod` - Run server in production mode
- `make test` - Run tests
- `make format` - Format code with black and isort
- `make lint` - Lint code with flake8
- `make clean` - Clean up temporary files
- `make health` - Check if server is running
- `make info` - Show server information

## Environment Setup

Before running the application, you need to set up your OpenAI API key:

1. Copy the example environment file:
```bash
cp env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
```

## API Endpoints

### Basic Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /api/hello/{name}` - Personalized greeting
- `POST /api/echo` - Echo received data

### AI Agent Endpoints
- `POST /api/chat` - Chat with the AI agent
- `GET /api/agent/info` - Get agent capabilities and information

## AI Agent Capabilities

The AI agent can help you with:

1. **Mathematical Calculations** - Solve math problems using the `calculate` tool
2. **Weather Information** - Get weather data for various cities (mock implementation)
3. **Knowledge Search** - Search through a knowledge base for information
4. **Chrome Browser History** - Read and search through your Google Chrome browsing history
5. **General Conversation** - Chat about various topics

### Example Usage

```bash
# Test the agent with curl
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is 15 + 27?"}'

curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is the weather in Tokyo?"}'

curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Tell me about Python programming"}'

curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Show me my recent browsing history"}'

curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Find my GitHub visits"}'
```

## Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Server Information

- Host: 0.0.0.0 (accessible from any IP)
- Port: 8000
- Auto-reload: Enabled for development
- AI Model: GPT-3.5-turbo

## Chrome History Tool

The AI agent includes a powerful Chrome history reading tool that can:

- **Read Recent History**: Get your most recent browsing history
- **Search by Keywords**: Find websites containing specific terms
- **Search by Domain**: Find visits to specific websites
- **Search by Topic**: Find websites related to specific topics

### Important Notes:
- **Chrome must be closed** for the tool to work properly
- The tool creates a temporary copy of your history database to avoid conflicts
- Your browsing history is only accessed locally - no data is sent to external services
- The tool works on macOS, Windows, and Linux

### Chrome History Examples:
- "Show me my recent browsing history"
- "Find websites about machine learning"
- "What GitHub repositories have I visited?"
- "Show me my YouTube watch history"
- "Find my visits to stackoverflow.com"
