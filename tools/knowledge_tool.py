"""
Knowledge search tool (mock implementation).
"""

from langchain_core.tools import tool


@tool
def search_knowledge(query: str) -> str:
    """Search through a knowledge base (mock implementation)."""
    # Mock knowledge base
    knowledge = {
        "python": "Python is a high-level programming language known for its simplicity and readability.",
        "fastapi": "FastAPI is a modern, fast web framework for building APIs with Python.",
        "langgraph": "LangGraph is a library for building stateful, multi-actor applications with LLMs.",
        "ai": "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines."
    }
    
    query_lower = query.lower()
    for key, value in knowledge.items():
        if key in query_lower:
            return f"Knowledge about '{key}': {value}"
    
    return f"No specific knowledge found for '{query}'. Available topics: {', '.join(knowledge.keys())}"
