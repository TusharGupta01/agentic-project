"""
LangChain Expression Language (LCEL) based agent with conversation memory.
This is a simpler alternative to the LangGraph approach.
"""

from typing import Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.messages import HumanMessage, AIMessage

from .llm import get_llm
from .prompts import get_browsing_history_prompt
from .memory import conversation_memory
from tools import get_weather, search_knowledge, read_chrome_history, analyze_browsing_patterns


def determine_tool_needed(user_input: str) -> Dict[str, Any]:
    """Determine which tool is needed based on user input."""
    user_lower = user_input.lower()
    
    # Check for browsing history queries
    if any(keyword in user_lower for keyword in ["history", "browsing", "visited", "websites", "domains"]):
        if "recent" in user_lower:
            return {
                "tool": "read_chrome_history",
                "args": {"query": "", "limit": 10, "analysis_type": "recent"},
                "needs_tool": True
            }
        elif "frequent" in user_lower or "most visited" in user_lower:
            return {
                "tool": "read_chrome_history", 
                "args": {"query": "", "limit": 10, "analysis_type": "frequent"},
                "needs_tool": True
            }
        elif "domains" in user_lower or "top domains" in user_lower:
            return {
                "tool": "read_chrome_history",
                "args": {"query": "", "limit": 10, "analysis_type": "domains"},
                "needs_tool": True
            }
        elif "pattern" in user_lower or "analyze" in user_lower:
            timeframe = "week"  # default
            if "day" in user_lower:
                timeframe = "day"
            elif "month" in user_lower:
                timeframe = "month"
            return {
                "tool": "analyze_browsing_patterns",
                "args": {"timeframe": timeframe},
                "needs_tool": True
            }
        else:
            # General history search
            return {
                "tool": "read_chrome_history",
                "args": {"query": user_input, "limit": 10, "analysis_type": "search"},
                "needs_tool": True
            }
    
    # Check for weather queries
    elif any(keyword in user_lower for keyword in ["weather", "temperature", "climate"]):
        # Extract city name (simple approach)
        words = user_input.split()
        city = "Unknown"
        for i, word in enumerate(words):
            if word.lower() in ["weather", "temperature"] and i + 1 < len(words):
                city = words[i + 1]
                break
        return {
            "tool": "get_weather",
            "args": {"city": city},
            "needs_tool": True
        }
    
    # Check for knowledge queries
    elif any(keyword in user_lower for keyword in ["what is", "tell me about", "explain", "knowledge"]):
        return {
            "tool": "search_knowledge",
            "args": {"query": user_input},
            "needs_tool": True
        }
    
    # No tool needed
    return {"tool": None, "args": {}, "needs_tool": False}


def execute_tool(tool_info: Dict[str, Any]) -> str:
    """Execute the appropriate tool based on tool_info."""
    if not tool_info["needs_tool"]:
        return "No tool needed"
    
    tool_name = tool_info["tool"]
    args = tool_info["args"]
    
    try:
        if tool_name == "read_chrome_history":
            return read_chrome_history.invoke(args)
        elif tool_name == "analyze_browsing_patterns":
            return analyze_browsing_patterns.invoke(args)
        elif tool_name == "get_weather":
            return get_weather.invoke(args)
        elif tool_name == "search_knowledge":
            return search_knowledge.invoke(args)
        else:
            return f"Unknown tool: {tool_name}"
    except Exception as e:
        return f"Error executing {tool_name}: {str(e)}"


def create_lcel_agent():
    """Create a LangChain Expression Language based agent with memory."""
    
    # Get the LLM
    llm = get_llm()
    
    # Create the main prompt template
    main_prompt = get_browsing_history_prompt()
    
    # Create a synthesis prompt for when tools are used
    synthesis_prompt = ChatPromptTemplate.from_template("""
    Based on the user's query, conversation history, and the tool results, provide a helpful and conversational response.

    Previous conversation:
    {conversation_history}

    User Query: {user_input}
    Tool Results: {tool_results}

    Create a natural, helpful response that addresses the user's question using the tool results and conversation context.
    """)
    
    # Build the LCEL chain
    agent_chain = (
        # Step 1: Determine if tools are needed and execute them
        RunnableLambda(lambda x: {
            "user_input": x["user_input"],
            "session_id": x["session_id"],
            "tool_info": determine_tool_needed(x["user_input"]),
        })
        |
        # Step 2: Execute tools if needed
        RunnableLambda(lambda x: {
            "user_input": x["user_input"],
            "session_id": x["session_id"],
            "tool_results": execute_tool(x["tool_info"]) if x["tool_info"]["needs_tool"] else "",
            "needs_tool": x["tool_info"]["needs_tool"]
        })
        |
        # Step 3: Get conversation history
        RunnableLambda(lambda x: {
            **x,
            "conversation_history": conversation_memory.get_conversation_context(x["session_id"], max_messages=10) if x["session_id"] else []
        })
        |
        # Step 4: Route to appropriate prompt
        RunnableLambda(lambda x: {
            "prompt": synthesis_prompt if x["needs_tool"] else main_prompt,
            "user_input": x["user_input"],
            "tool_results": x["tool_results"],
            "conversation_history": x["conversation_history"]
        })
        |
        # Step 5: Format and invoke LLM
        RunnableLambda(lambda x: {
            "messages": x["prompt"].format_messages(
                user_input=x["user_input"],
                tool_results=x["tool_results"],
                conversation_history=x["conversation_history"]
            ) if x["needs_tool"] else x["prompt"].format_messages(
                user_input=x["user_input"],
                conversation_history=x["conversation_history"]
            )
        })
        |
        # Step 6: Get LLM response
        RunnableLambda(lambda x: llm.invoke(x["messages"]))
        |
        # Step 7: Parse output
        StrOutputParser()
    )
    
    return agent_chain


def run_lcel_agent(user_input: str, session_id: Optional[str] = None) -> str:
    """Run the LCEL agent with user input and conversation memory."""
    try:
        # Create or get session
        if not session_id:
            session_id = conversation_memory.create_session()
        
        # Add user message to conversation history
        user_message = HumanMessage(content=user_input)
        conversation_memory.add_message(session_id, user_message)
        
        # Get conversation history
        conversation_history = conversation_memory.get_conversation_context(session_id, max_messages=10)
        
        # Determine if tools are needed
        tool_info = determine_tool_needed(user_input)
        
        # Execute tools if needed
        tool_results = ""
        if tool_info["needs_tool"]:
            tool_results = execute_tool(tool_info)
        
        # Get the LLM
        llm = get_llm()
        
        # Create appropriate prompt
        if tool_info["needs_tool"]:
            synthesis_prompt = ChatPromptTemplate.from_template("""
            Based on the user's query, conversation history, and the tool results, provide a helpful and conversational response.

            Previous conversation:
            {conversation_history}

            User Query: {user_input}
            Tool Results: {tool_results}

            Create a natural, helpful response that addresses the user's question using the tool results and conversation context.
            """)
            
            formatted_prompt = synthesis_prompt.format_messages(
                user_input=user_input,
                tool_results=tool_results,
                conversation_history=conversation_history
            )
        else:
            main_prompt = get_browsing_history_prompt()
            formatted_prompt = main_prompt.format_messages(
                user_input=user_input,
                conversation_history=conversation_history
            )
        
        # Get LLM response
        response = llm.invoke(formatted_prompt)
        result = response.content if hasattr(response, 'content') else str(response)
        
        # Add AI response to conversation history
        ai_message = AIMessage(content=result)
        conversation_memory.add_message(session_id, ai_message)
        
        return result
        
    except Exception as e:
        import traceback
        return f"Error running LCEL agent: {str(e)}\n{traceback.format_exc()}"


# Example usage
if __name__ == "__main__":
    # Test the LCEL agent
    test_queries = [
        "Show me my recent browsing history",
        "What are my most visited websites?",
        "Find websites about Python programming",
        "What's the weather in Tokyo?",
        "Tell me about FastAPI",
        "Hello, how are you?"
    ]
    
    # Create a test session
    session_id = conversation_memory.create_session()
    
    for query in test_queries:
        print(f"\nUser: {query}")
        try:
            response = run_lcel_agent(query, session_id)
            print(f"Agent: {response[:200]}...")
        except Exception as e:
            print(f"Error: {e}")
