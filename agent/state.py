"""
Agent state definitions.
"""

from typing import List, Any, TypedDict


class AgentState(TypedDict):
    """State structure for the browsing history analysis agent."""
    messages: List[Any]
    user_input: str
    final_response: str
