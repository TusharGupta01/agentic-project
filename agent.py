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
def read_chrome_history(query: str = "", limit: int = 10, analysis_type: str = "search") -> str:
    """Read and analyze Google Chrome browser history with intelligent insights."""
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
        import shutil
        import tempfile
        
        temp_db = tempfile.mktemp(suffix=".db")
        shutil.copy2(history_db, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Query the history based on analysis type
        if analysis_type == "recent":
            cursor.execute("""
                SELECT url, title, datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') as visit_time,
                       visit_count
                FROM urls 
                ORDER BY last_visit_time DESC 
                LIMIT ?
            """, (limit,))
        elif analysis_type == "frequent":
            cursor.execute("""
                SELECT url, title, datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') as visit_time,
                       visit_count
                FROM urls 
                WHERE visit_count > 1
                ORDER BY visit_count DESC 
                LIMIT ?
            """, (limit,))
        elif analysis_type == "domains":
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN url LIKE 'https://%' THEN substr(url, 9, instr(substr(url, 9), '/') - 1)
                        WHEN url LIKE 'http://%' THEN substr(url, 8, instr(substr(url, 8), '/') - 1)
                        ELSE 'unknown'
                    END as domain,
                    COUNT(*) as visit_count,
                    MAX(datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch')) as last_visit
                FROM urls 
                GROUP BY domain
                ORDER BY visit_count DESC 
                LIMIT ?
            """, (limit,))
        else:  # search
            if query:
                cursor.execute("""
                    SELECT url, title, datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') as visit_time,
                           visit_count
                    FROM urls 
                    WHERE url LIKE ? OR title LIKE ?
                    ORDER BY last_visit_time DESC 
                    LIMIT ?
                """, (f"%{query}%", f"%{query}%", limit))
            else:
                cursor.execute("""
                    SELECT url, title, datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') as visit_time,
                           visit_count
                    FROM urls 
                    ORDER BY last_visit_time DESC 
                    LIMIT ?
                """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        os.unlink(temp_db)  # Clean up temp file
        
        if not results:
            return f"No history entries found for query: '{query}'"
        
        # Format results based on analysis type
        if analysis_type == "domains":
            response = f"Top {len(results)} most visited domains:\n\n"
            for i, (domain, visit_count, last_visit) in enumerate(results, 1):
                response += f"{i}. {domain}\n"
                response += f"   Visits: {visit_count}\n"
                response += f"   Last visit: {last_visit}\n\n"
        else:
            response = f"Found {len(results)} history entries"
            if query:
                response += f" matching '{query}'"
            response += ":\n\n"
            
            for i, result in enumerate(results, 1):
                if len(result) == 4:  # url, title, visit_time, visit_count
                    url, title, visit_time, visit_count = result
                else:  # domains query
                    continue
                
                # Truncate long URLs and titles for readability
                display_url = url[:80] + "..." if len(url) > 80 else url
                display_title = title[:60] + "..." if len(title) > 60 else title
                
                response += f"{i}. {display_title}\n"
                response += f"   URL: {display_url}\n"
                response += f"   Visited: {visit_time}\n"
                if visit_count > 1:
                    response += f"   Visit count: {visit_count}\n"
                response += "\n"
        
        return response
        
    except Exception as e:
        return f"Error reading Chrome history: {str(e)}. Make sure Chrome is not running and try again."

@tool
def analyze_browsing_patterns(timeframe: str = "week") -> str:
    """Analyze browsing patterns and provide insights about web usage."""
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
        
        import shutil
        import tempfile
        
        temp_db = tempfile.mktemp(suffix=".db")
        shutil.copy2(history_db, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Calculate time filter based on timeframe
        if timeframe == "day":
            time_filter = "datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') >= datetime('now', '-1 day')"
        elif timeframe == "week":
            time_filter = "datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') >= datetime('now', '-7 days')"
        elif timeframe == "month":
            time_filter = "datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') >= datetime('now', '-30 days')"
        else:
            time_filter = "1=1"  # All time
        
        # Get domain statistics
        cursor.execute(f"""
            SELECT 
                CASE 
                    WHEN url LIKE 'https://%' THEN substr(url, 9, instr(substr(url, 9), '/') - 1)
                    WHEN url LIKE 'http://%' THEN substr(url, 8, instr(substr(url, 8), '/') - 1)
                    ELSE 'unknown'
                END as domain,
                COUNT(*) as visit_count,
                MAX(datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch')) as last_visit
            FROM urls 
            WHERE {time_filter}
            GROUP BY domain
            ORDER BY visit_count DESC 
            LIMIT 10
        """)
        
        domain_results = cursor.fetchall()
        
        # Get total visits
        cursor.execute(f"""
            SELECT COUNT(*) as total_visits
            FROM urls 
            WHERE {time_filter}
        """)
        
        total_visits = cursor.fetchone()[0]
        
        conn.close()
        os.unlink(temp_db)
        
        # Format analysis
        response = f"📊 Browsing Analysis for the last {timeframe}:\n\n"
        response += f"Total visits: {total_visits}\n\n"
        response += "Top 10 most visited domains:\n\n"
        
        for i, (domain, visit_count, last_visit) in enumerate(domain_results, 1):
            percentage = (visit_count / total_visits * 100) if total_visits > 0 else 0
            response += f"{i}. {domain}\n"
            response += f"   Visits: {visit_count} ({percentage:.1f}%)\n"
            response += f"   Last visit: {last_visit}\n\n"
        
        return response
        
    except Exception as e:
        return f"Error analyzing browsing patterns: {str(e)}. Make sure Chrome is not running and try again."

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
    You are a specialized AI assistant focused on helping users analyze and understand their browsing history. 
    Your primary capabilities include:
    
    1. **Chrome History Analysis** - Read and search through Google Chrome browser history
    2. **Browsing Pattern Analysis** - Analyze browsing patterns and provide insights
    3. **Weather Information** - Get weather data for various cities (mock implementation)
    4. **General Knowledge** - Search through a knowledge base for information
    5. **General Conversation** - Chat about various topics
    
    **Primary Focus: Browsing History Analysis**
    You excel at helping users understand their web browsing behavior by:
    - Finding specific websites they've visited
    - Analyzing their most frequented domains
    - Identifying browsing patterns over time
    - Providing insights about their web usage habits
    - Answering questions about their browsing history
    
    **Available History Analysis Types:**
    - "recent" - Get recent browsing history
    - "frequent" - Find most frequently visited sites
    - "domains" - Analyze top domains by visit count
    - "search" - Search for specific terms in history
    
    Always be helpful, accurate, and friendly. Focus on providing meaningful insights about the user's browsing behavior.
    """)
    
    # Prepare messages
    messages = [system_message] + state["messages"]
    
    # Get response from LLM
    response = llm.invoke(messages)
    
    return {"messages": [response]}

def call_tools(state: AgentState):
    """Call the tools that the agent requested."""
    # Get the tools
    tools = [get_weather, search_knowledge, read_chrome_history, analyze_browsing_patterns]
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
