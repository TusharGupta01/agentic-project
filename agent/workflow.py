"""
LangGraph workflow for the browsing history analysis agent.
"""

from typing import Dict, Any, Optional
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from .state import AgentState
from .llm import get_llm
from .prompts import get_browsing_history_prompt, get_response_synthesis_prompt
from .memory import conversation_memory
from tools import (
    get_weather, search_knowledge, read_chrome_history, analyze_browsing_patterns,
    list_folder_contents, read_file_content, analyze_folder_structure, 
    search_files_in_folder, get_file_summary
)


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
    
    # Get the tools and bind them to the LLM
    tools = [
        get_weather, search_knowledge, read_chrome_history, analyze_browsing_patterns,
        list_folder_contents, read_file_content, analyze_folder_structure, 
        search_files_in_folder, get_file_summary
    ]
    llm_with_tools = llm.bind_tools(tools)
    
    # Get the user input from the last message
    user_input = state["user_input"]
    session_id = state.get("session_id")
    
    # Get conversation history if session exists
    conversation_history = []
    if session_id:
        conversation_history = conversation_memory.get_conversation_context(session_id, max_messages=10)
    
    # Check if we have tool results in the current state
    has_tool_results = any(isinstance(msg, ToolMessage) for msg in state["messages"])
    
    if has_tool_results:
        # Extract tool results from the messages
        tool_results = []
        for msg in state["messages"]:
            if isinstance(msg, ToolMessage):
                tool_results.append(f"Tool: {msg.name} - Result: {msg.content}")
        
        # If we have tool results, use a synthesis prompt
        synthesis_prompt = ChatPromptTemplate.from_template("""
        Based on the user's query, conversation history, and the tool results, provide a helpful and conversational response.

        Previous conversation:
        {conversation_history}

        User Query: {user_input}

        Tool Results:
        {tool_results}

        Create a natural, helpful response that addresses the user's question using the tool results and conversation context.
        Do NOT call any more tools - provide a final response based on the information you have.
        """)
        
        formatted_prompt = synthesis_prompt.format_messages(
            user_input=user_input,
            conversation_history=conversation_history,
            tool_results="\n".join(tool_results)
        )
        
        # Use regular LLM (not with tools) for synthesis
        response = llm.invoke(formatted_prompt)
    else:
        # Create prompt template for initial response
        prompt_template = get_browsing_history_prompt()
        
        # Format the prompt with user input and conversation history
        formatted_prompt = prompt_template.format_messages(
            user_input=user_input,
            conversation_history=conversation_history
        )
        
        # Get response from LLM with tools
        response = llm_with_tools.invoke(formatted_prompt)
    
    return {"messages": [response]}


def call_tools(state: AgentState):
    """Call the tools that the agent requested."""
    # Get the tools
    tools = [
        get_weather, search_knowledge, read_chrome_history, analyze_browsing_patterns,
        list_folder_contents, read_file_content, analyze_folder_structure, 
        search_files_in_folder, get_file_summary
    ]
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
            "tools": "tools", 
            "end": "finalize"
        }
    )
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Compile the graph
    app = workflow.compile()
    
    return app


def run_agent(user_input: str, session_id: Optional[str] = None) -> str:
    """Run the agent with user input and return the response."""
    try:
        # Create or get session
        if not session_id:
            session_id = conversation_memory.create_session()
        
        # Add user message to conversation history
        user_message = HumanMessage(content=user_input)
        conversation_memory.add_message(session_id, user_message)
        
        # Create initial state
        initial_state = {
            "messages": [user_message],
            "user_input": user_input,
            "final_response": "",
            "session_id": session_id
        }
        
        # Run the agent
        result = create_agent_graph().invoke(initial_state)
        
        # Add AI response to conversation history
        final_response = result.get("final_response", "No response generated")
        ai_message = AIMessage(content=final_response)
        conversation_memory.add_message(session_id, ai_message)
        
        return final_response
        
    except Exception as e:
        return f"Error running agent: {str(e)}"
