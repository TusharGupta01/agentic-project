"""
LangGraph workflow for the browsing history analysis agent.
"""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from .state import AgentState
from .llm import get_llm
from tools import get_weather, search_knowledge, read_chrome_history, analyze_browsing_patterns


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
        result = create_agent_graph().invoke(initial_state)
        
        return result.get("final_response", "No response generated")
        
    except Exception as e:
        return f"Error running agent: {str(e)}"
