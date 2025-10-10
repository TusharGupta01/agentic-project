"""
Safe Chrome browser history analysis tools (mock data only).
Use this version to avoid security alerts.
"""

from langchain_core.tools import tool


def _get_mock_history_data(query: str, limit: int, analysis_type: str) -> str:
    """Return mock history data for development/testing to avoid security alerts."""
    mock_data = {
        "recent": [
            "1. GitHub - https://github.com",
            "2. Stack Overflow - https://stackoverflow.com", 
            "3. Python Documentation - https://docs.python.org",
            "4. OpenAI API - https://platform.openai.com",
            "5. FastAPI Documentation - https://fastapi.tiangolo.com",
            "6. LangChain Documentation - https://python.langchain.com",
            "7. React Documentation - https://react.dev",
            "8. Node.js Documentation - https://nodejs.org",
            "9. Docker Documentation - https://docs.docker.com",
            "10. AWS Documentation - https://docs.aws.amazon.com"
        ],
        "frequent": [
            "1. GitHub (25 visits)",
            "2. Stack Overflow (18 visits)",
            "3. Python Documentation (15 visits)", 
            "4. OpenAI API (12 visits)",
            "5. FastAPI Documentation (10 visits)",
            "6. LangChain Documentation (8 visits)",
            "7. React Documentation (6 visits)",
            "8. Node.js Documentation (5 visits)",
            "9. Docker Documentation (4 visits)",
            "10. AWS Documentation (3 visits)"
        ],
        "domains": [
            "1. github.com (25 visits)",
            "2. stackoverflow.com (18 visits)",
            "3. docs.python.org (15 visits)",
            "4. platform.openai.com (12 visits)",
            "5. fastapi.tiangolo.com (10 visits)",
            "6. python.langchain.com (8 visits)",
            "7. react.dev (6 visits)",
            "8. nodejs.org (5 visits)",
            "9. docs.docker.com (4 visits)",
            "10. docs.aws.amazon.com (3 visits)"
        ],
        "search": [
            f"Found {limit} results for '{query}':",
            "1. Python Programming Tutorial - https://python.org/tutorial",
            "2. Python Best Practices - https://docs.python.org/3/tutorial",
            "3. Python Libraries - https://pypi.org",
            "4. Python Web Development - https://fastapi.tiangolo.com",
            "5. Python AI/ML - https://python.langchain.com"
        ]
    }
    
    data = mock_data.get(analysis_type, mock_data["search"])
    return f"Found {len(data)} history entries:\n\n" + "\n".join(data[:limit])


@tool
def read_chrome_history(query: str = "", limit: int = 10, analysis_type: str = "search") -> str:
    """Read and analyze Google Chrome browser history with intelligent insights (mock data only)."""
    return _get_mock_history_data(query, limit, analysis_type)


@tool
def analyze_browsing_patterns(timeframe: str = "week") -> str:
    """Analyze browsing patterns over time (mock data only)."""
    patterns = {
        "day": {
            "most_active_hour": "2:00 PM",
            "total_visits": 45,
            "top_categories": ["Development", "Documentation", "Social Media"],
            "insights": [
                "Peak browsing activity during afternoon hours",
                "Heavy focus on development and documentation sites",
                "Balanced mix of work and personal browsing"
            ]
        },
        "week": {
            "most_active_day": "Tuesday",
            "total_visits": 280,
            "top_categories": ["Development", "Documentation", "News", "Social Media"],
            "insights": [
                "Most productive browsing on weekdays",
                "Development sites dominate usage",
                "Weekend browsing focuses on news and social media"
            ]
        },
        "month": {
            "most_active_week": "Week 2",
            "total_visits": 1200,
            "top_categories": ["Development", "Documentation", "News", "Social Media", "Shopping"],
            "insights": [
                "Consistent development-focused browsing pattern",
                "Documentation sites are most visited",
                "Shopping activity peaks mid-month"
            ]
        }
    }
    
    data = patterns.get(timeframe, patterns["week"])
    
    result = f"Browsing Pattern Analysis ({timeframe}):\n\n"
    result += f"Most Active: {data['most_active_hour'] if timeframe == 'day' else data['most_active_day'] if timeframe == 'week' else data['most_active_week']}\n"
    result += f"Total Visits: {data['total_visits']}\n\n"
    result += "Top Categories:\n"
    for category in data['top_categories']:
        result += f"- {category}\n"
    
    result += "\nKey Insights:\n"
    for insight in data['insights']:
        result += f"- {insight}\n"
    
    return result
