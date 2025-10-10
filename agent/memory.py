"""
Conversation memory management for the agent.
"""

from typing import Dict, List, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import uuid
from datetime import datetime, timedelta


class ConversationMemory:
    """Manages conversation history for multiple sessions."""
    
    def __init__(self, max_sessions: int = 100, session_timeout_hours: int = 24):
        self.sessions: Dict[str, Dict] = {}
        self.max_sessions = max_sessions
        self.session_timeout_hours = session_timeout_hours
    
    def create_session(self) -> str:
        """Create a new conversation session."""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "messages": [],
            "created_at": datetime.now(),
            "last_accessed": datetime.now()
        }
        
        # Clean up old sessions if we exceed the limit
        self._cleanup_sessions()
        
        return session_id
    
    def add_message(self, session_id: str, message: BaseMessage) -> None:
        """Add a message to a conversation session."""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        self.sessions[session_id]["messages"].append(message)
        self.sessions[session_id]["last_accessed"] = datetime.now()
    
    def get_messages(self, session_id: str, limit: Optional[int] = None) -> List[BaseMessage]:
        """Get messages from a conversation session."""
        if session_id not in self.sessions:
            return []
        
        messages = self.sessions[session_id]["messages"]
        self.sessions[session_id]["last_accessed"] = datetime.now()
        
        if limit:
            return messages[-limit:]
        return messages
    
    def get_conversation_context(self, session_id: str, max_messages: int = 10) -> List[BaseMessage]:
        """Get recent conversation context for the agent."""
        messages = self.get_messages(session_id, limit=max_messages)
        return messages
    
    def clear_session(self, session_id: str) -> None:
        """Clear all messages from a session."""
        if session_id in self.sessions:
            self.sessions[session_id]["messages"] = []
            self.sessions[session_id]["last_accessed"] = datetime.now()
    
    def delete_session(self, session_id: str) -> None:
        """Delete a conversation session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def _cleanup_sessions(self) -> None:
        """Remove old sessions to prevent memory bloat."""
        if len(self.sessions) <= self.max_sessions:
            return
        
        # Sort sessions by last accessed time
        sorted_sessions = sorted(
            self.sessions.items(),
            key=lambda x: x[1]["last_accessed"]
        )
        
        # Remove oldest sessions
        sessions_to_remove = len(self.sessions) - self.max_sessions
        for session_id, _ in sorted_sessions[:sessions_to_remove]:
            del self.sessions[session_id]
    
    def cleanup_expired_sessions(self) -> None:
        """Remove sessions that haven't been accessed recently."""
        cutoff_time = datetime.now() - timedelta(hours=self.session_timeout_hours)
        
        expired_sessions = [
            session_id for session_id, data in self.sessions.items()
            if data["last_accessed"] < cutoff_time
        ]
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """Get information about a session."""
        if session_id not in self.sessions:
            return None
        
        session_data = self.sessions[session_id]
        return {
            "session_id": session_id,
            "message_count": len(session_data["messages"]),
            "created_at": session_data["created_at"].isoformat(),
            "last_accessed": session_data["last_accessed"].isoformat()
        }
    
    def get_all_sessions(self) -> List[Dict]:
        """Get information about all active sessions."""
        return [self.get_session_info(session_id) for session_id in self.sessions.keys()]


# Global memory instance
conversation_memory = ConversationMemory()
