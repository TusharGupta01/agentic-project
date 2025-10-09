"""
Simple AI Agent using LangGraph
This agent can perform basic reasoning and tool usage tasks.
"""

import os
import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, TypedDict, Optional
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

# Load environment variables
load_dotenv()

# Define the agent state
class AgentState(TypedDict):
    messages: List[Any]
    user_input: str
    final_response: str

# Define tools for the agent
@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression safely."""
    try:
        # Simple safe evaluation for basic math
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return "Error: Only basic mathematical operations are allowed"
        
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

@tool
def get_weather(city: str) -> str:
    """Get weather information for a city (mock implementation)."""
    # This is a mock implementation - in a real app, you'd call a weather API
    weather_data = {
        "new york": "Sunny, 22°C",
        "london": "Cloudy, 15°C", 
        "tokyo": "Rainy, 18°C",
        "paris": "Partly cloudy, 20°C"
    }
    
    city_lower = city.lower()
    if city_lower in weather_data:
        return f"Weather in {city}: {weather_data[city_lower]}"
    else:
        return f"Weather data not available for {city}. Available cities: {', '.join(weather_data.keys())}"

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

@tool
def read_chrome_history(query: str = "", limit: int = 10) -> str:
    """Read and search through Google Chrome browser history."""
    try:
        # Common Chrome history database locations
        chrome_paths = [
            os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/History"),
            os.path.expanduser("~/AppData/Local/Google/Chrome/User Data/Default/History"),
            os.path.expanduser("~/.config/google-chrome/Default/History"),
            os.path.expanduser("~/snap/chromium/common/chromium/Default/History")
        ]
        
        history_db = None
        for path in chrome_paths:
            if os.path.exists(path):
                history_db = path
                break
        
        if not history_db:
            return "Chrome history database not found. Please ensure Chrome is installed and has been used."
        
        # Connect to the Chrome history database
        # Note: Chrome locks the database when running, so we need to copy it
        import shutil
        import tempfile
        
        temp_db = tempfile.mktemp(suffix=".db")
        shutil.copy2(history_db, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Query the history
        if query:
            # Search for URLs containing the query
            cursor.execute("""
                SELECT url, title, datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') as visit_time
                FROM urls 
                WHERE url LIKE ? OR title LIKE ?
                ORDER BY last_visit_time DESC 
                LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit))
        else:
            # Get recent history
            cursor.execute("""
                SELECT url, title, datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') as visit_time
                FROM urls 
                ORDER BY last_visit_time DESC 
                LIMIT ?
            """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        os.unlink(temp_db)  # Clean up temp file
        
        if not results:
            return f"No history entries found for query: '{query}'"
        
        # Format results
        history_entries = []
        for url, title, visit_time in results:
            # Truncate long URLs and titles for readability
            display_url = url[:80] + "..." if len(url) > 80 else url
            display_title = title[:60] + "..." if len(title) > 60 else title
            
            history_entries.append({
                "title": display_title,
                "url": display_url,
                "visit_time": visit_time
            })
        
        # Create response
        response = f"Found {len(history_entries)} history entries"
        if query:
            response += f" matching '{query}'"
        response += ":\n\n"
        
        for i, entry in enumerate(history_entries, 1):
            response += f"{i}. {entry['title']}\n"
            response += f"   URL: {entry['url']}\n"
            response += f"   Visited: {entry['visit_time']}\n\n"
        
        return response
        
    except Exception as e:
        return f"Error reading Chrome history: {str(e)}. Make sure Chrome is not running and try again."

# Initialize the LLM
def get_llm():
    """Initialize the language model."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        api_key=api_key
    )

# Define agent functions
def should_continue(state: AgentState) -> str:
    """Determine if the agent should continue or end."""
    messages = state["messages"]
    last_message = messages[-1]
    
    # If the last message is from the user, continue to the agent
    if isinstance(last_message, HumanMessage):
        return "agent"
    # If the last message is from the AI and doesn't need tools, end
    elif isinstance(last_message, AIMessage) and not last_message.tool_calls:
        return "end"
    # If the AI wants to use tools, go to tools
    else:
        return "tools"

def call_agent(state: AgentState):
    """Call the language model agent."""
    llm = get_llm()
    
    # Create system message
    system_message = SystemMessage(content="""
    You are a helpful AI assistant. You can help users with:
    1. Mathematical calculations using the calculate tool
    2. Weather information using the get_weather tool  
    3. General knowledge using the search_knowledge tool
    4. Reading and searching Google Chrome browser history using the read_chrome_history tool
    5. General conversation and questions
    
    Always be helpful, accurate, and friendly. If you need to use tools, do so.
    If you don't need tools, respond directly to the user.
    
    For Chrome history requests, you can search for specific websites, topics, or get recent browsing history.
    """)
    
    # Prepare messages
    messages = [system_message] + state["messages"]
    
    # Get response from LLM
    response = llm.invoke(messages)
    
    return {"messages": [response]}

def call_tools(state: AgentState):
    """Call the tools that the agent requested."""
    # Get the tools
    tools = [calculate, get_weather, search_knowledge, read_chrome_history]
    tool_node = ToolNode(tools)
    
    # Execute the tools
    result = tool_node.invoke(state)
    
    return result

def finalize_response(state: AgentState):
    """Finalize the response for the user."""
    messages = state["messages"]
    
    # Get the final AI response
    final_message = None
    for message in reversed(messages):
        if isinstance(message, AIMessage) and not message.tool_calls:
            final_message = message
            break
    
    if final_message:
        return {"final_response": final_message.content}
    else:
        return {"final_response": "I apologize, but I couldn't generate a proper response."}

# Create the LangGraph workflow
def create_agent_graph():
    """Create and return the LangGraph agent workflow."""
    
    # Create the state graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", call_agent)
    workflow.add_node("tools", call_tools)
    workflow.add_node("finalize", finalize_response)
    
    # Add edges
    workflow.add_edge("tools", "agent")
    workflow.add_edge("finalize", END)
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "agent": "agent",
            "tools": "tools", 
            "end": "finalize"
        }
    )
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Compile the graph
    app = workflow.compile()
    
    return app

# Initialize the agent
agent_app = create_agent_graph()

def run_agent(user_input: str) -> str:
    """Run the agent with user input and return the response."""
    try:
        # Create initial state
        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "user_input": user_input,
            "final_response": ""
        }
        
        # Run the agent
        result = agent_app.invoke(initial_state)
        
        return result.get("final_response", "No response generated")
        
    except Exception as e:
        return f"Error running agent: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Test the agent
    test_queries = [
        "What is 15 + 27?",
        "What's the weather like in Tokyo?",
        "Tell me about Python programming",
        "Hello, how are you?"
    ]
    
    for query in test_queries:
        print(f"\nUser: {query}")
        response = run_agent(query)
        print(f"Agent: {response}")
