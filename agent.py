"""
Simple AI Agent using LangGraph
This agent can perform basic reasoning and tool usage tasks.
"""

import os
from typing import Dict, Any, List, TypedDict
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
    4. General conversation and questions
    
    Always be helpful, accurate, and friendly. If you need to use tools, do so.
    If you don't need tools, respond directly to the user.
    """)
    
    # Prepare messages
    messages = [system_message] + state["messages"]
    
    # Get response from LLM
    response = llm.invoke(messages)
    
    return {"messages": [response]}

def call_tools(state: AgentState):
    """Call the tools that the agent requested."""
    # Get the tools
    tools = [calculate, get_weather, search_knowledge]
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
