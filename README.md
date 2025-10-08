# Basic FastAPI Project

A simple FastAPI application with basic endpoints and automatic documentation.

## Features

- FastAPI web framework
- Automatic API documentation (Swagger UI)
- Basic endpoints for testing
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

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /api/hello/{name}` - Personalized greeting
- `POST /api/echo` - Echo received data

## Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Server Information

- Host: 0.0.0.0 (accessible from any IP)
- Port: 8000
- Auto-reload: Enabled for development
