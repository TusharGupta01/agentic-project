"""
Tools package for the AI Agent.
"""

from .weather_tool import get_weather
from .knowledge_tool import search_knowledge
from .chrome_history_tool import read_chrome_history, analyze_browsing_patterns
from .file_analysis_tool import (
    list_folder_contents,
    read_file_content,
    analyze_folder_structure,
    search_files_in_folder,
    get_file_summary
)
from .email_writing_tool import (
    write_email,
    write_text_message,
    suggest_email_improvements,
    get_communication_templates
)

__all__ = [
    "get_weather",
    "search_knowledge", 
    "read_chrome_history",
    "analyze_browsing_patterns",
    "list_folder_contents",
    "read_file_content",
    "analyze_folder_structure",
    "search_files_in_folder",
    "get_file_summary",
    "write_email",
    "write_text_message",
    "suggest_email_improvements",
    "get_communication_templates"
]
