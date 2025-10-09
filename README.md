# Browsing History Analysis Agent

A specialized AI agent powered by LangGraph and FastAPI that helps you analyze and understand your Google Chrome browsing history with intelligent insights and pattern recognition.

## Features

- **Specialized Browsing History Analysis** - Deep insights into your web browsing patterns
- **Multiple Analysis Types** - Recent history, frequent sites, domain statistics, and search
- **Pattern Recognition** - Identify browsing habits and trends over time
- **FastAPI web framework** with automatic documentation (Swagger UI)
- **AI Agent powered by LangGraph and OpenAI**
- **Cross-platform support** - Works on macOS, Windows, and Linux
- **Privacy-focused** - All analysis happens locally on your machine
- **Hot reload for development**

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

The AI agent specializes in helping you understand your browsing behavior:

1. **Chrome History Analysis** - Read and analyze your Google Chrome browsing history
2. **Browsing Pattern Insights** - Understand your web usage habits and trends
3. **Domain Statistics** - See which websites you visit most frequently
4. **Search Through History** - Find specific websites, topics, or time periods
5. **Time-based Analysis** - Analyze browsing patterns over different timeframes
6. **General Knowledge** - Search through a knowledge base for information
7. **Weather Information** - Get weather data for various cities (mock implementation)

### Example Usage

```bash
# Test the agent with curl
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Show me my recent browsing history"}'

curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What are my most visited websites?"}'

curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Find my GitHub visits"}'

curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Analyze my browsing patterns for the last week"}'

curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What websites did I visit about machine learning?"}'
```

## Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Server Information

- Host: 0.0.0.0 (accessible from any IP)
- Port: 8000
- Auto-reload: Enabled for development
- AI Model: GPT-3.5-turbo-1106 (cheapest available)
- Cost: $0.001/1K input tokens, $0.002/1K output tokens

## Browsing History Analysis Features

The AI agent specializes in comprehensive browsing history analysis:

### **Core Analysis Types:**
- **Recent History** - Get your most recent browsing activity
- **Frequent Sites** - Find websites you visit most often
- **Domain Statistics** - Analyze which domains you visit most
- **Keyword Search** - Find websites containing specific terms
- **Time-based Analysis** - Analyze patterns over different timeframes

### **Advanced Insights:**
- **Browsing Pattern Analysis** - Understand your web usage habits
- **Visit Frequency Tracking** - See how often you visit specific sites
- **Domain Popularity** - Identify your most frequented websites
- **Time-based Trends** - Analyze browsing patterns over days, weeks, or months

### **Example Queries:**
- "Show me my recent browsing history"
- "What are my most visited websites?"
- "Analyze my browsing patterns for the last week"
- "Find websites about machine learning"
- "What GitHub repositories have I visited?"
- "Show me my YouTube watch history"
- "Which domains do I visit most frequently?"

### **Important Notes:**
- **Chrome must be closed** for the tool to work properly
- The tool creates a temporary copy of your history database to avoid conflicts
- Your browsing history is only accessed locally - no data is sent to external services
- The tool works on macOS, Windows, and Linux
- All analysis happens on your local machine for privacy

## Cost Optimization

The agent is configured to use the **cheapest available OpenAI model** to minimize costs:

### **Current Configuration:**
- **Model**: GPT-3.5-turbo-1106
- **Cost**: $0.001/1K input tokens, $0.002/1K output tokens
- **Max Tokens**: 1000 (limits response length to control costs)
- **Temperature**: 0.3 (focused responses)

### **Cost Examples:**
- **Simple query** (1000 input, 500 output): ~$0.002
- **Complex analysis** (2000 input, 1000 output): ~$0.004
- **Heavy usage** (5000 input, 2000 output): ~$0.009

### **Cost Savings:**
- **92% cheaper** than GPT-4 Turbo
- **33% cheaper** than standard GPT-3.5-turbo
- **Perfect for browsing history analysis** tasks

### **Model Options:**
The system supports multiple model tiers:
- **Cheapest**: GPT-3.5-turbo-1106 (current)
- **Balanced**: GPT-3.5-turbo
- **Premium**: GPT-4-turbo-preview

Check `/api/model/info` endpoint for detailed cost information.
