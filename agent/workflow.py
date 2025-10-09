"""
LangGraph workflow for the browsing history analysis agent.
"""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from .state import AgentState
from .llm import get_llm
from .prompts import get_browsing_history_prompt, get_response_synthesis_prompt
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
    """Call the language model agent using structured prompt templates."""
    llm = get_llm()
    
    # Get the user input from the last message
    user_input = state["user_input"]
    
    # Create prompt template
    prompt_template = get_browsing_history_prompt()
    
    # Format the prompt with user input
    formatted_prompt = prompt_template.format_messages(user_input=user_input)
    
    # Get response from LLM
    response = llm.invoke(formatted_prompt)
    
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
    """Finalize the response for the user using prompt templates."""
    messages = state["messages"]
    user_input = state["user_input"]
    
    # Get the final AI response
    final_message = None
    tool_results = []
    
    for message in messages:
        if isinstance(message, AIMessage):
            if message.tool_calls:
                # Collect tool call information
                for tool_call in message.tool_calls:
                    tool_results.append(f"Tool: {tool_call['name']} - {tool_call.get('args', {})}")
            else:
                final_message = message
    
    if final_message and tool_results:
        # Use synthesis prompt to create a better response
        llm = get_llm()
        synthesis_prompt = get_response_synthesis_prompt()
        
        formatted_prompt = synthesis_prompt.format_messages(
            user_input=user_input,
            tool_results="\n".join(tool_results)
        )
        
        synthesis_response = llm.invoke(formatted_prompt)
        return {"final_response": synthesis_response.content}
    elif final_message:
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
