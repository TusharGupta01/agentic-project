"""
Agent state definitions.
"""

from typing import List, Any, TypedDict, Optional
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """State structure for the browsing history analysis agent."""
    messages: List[BaseMessage]  # Conversation history
    user_input: str
    final_response: str
    session_id: Optional[str]  # For tracking conversation sessions
