from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

# Create FastAPI instance
app = FastAPI(
    title="Basic FastAPI Project",
    description="A simple FastAPI application with basic endpoints",
    version="1.0.0"
)

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
