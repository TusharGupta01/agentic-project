"""
Chrome browser history analysis tools.
"""

import os
import sqlite3
import shutil
import tempfile
from langchain_core.tools import tool


def _get_chrome_history_path():
    """Get the path to Chrome history database."""
    chrome_paths = [
        os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/History"),
        os.path.expanduser("~/AppData/Local/Google/Chrome/User Data/Default/History"),
        os.path.expanduser("~/.config/google-chrome/Default/History"),
        os.path.expanduser("~/snap/chromium/common/chromium/Default/History")
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            return path
    
    return None


def _create_temp_db_copy(history_db_path):
    """Create a temporary copy of the Chrome history database."""
    temp_db = tempfile.mktemp(suffix=".db")
    shutil.copy2(history_db_path, temp_db)
    return temp_db


def _get_mock_history_data(query: str, limit: int, analysis_type: str) -> str:
    """Return mock history data for development/testing to avoid security alerts."""
    mock_data = {
        "recent": [
            "1. GitHub - https://github.com",
            "2. Stack Overflow - https://stackoverflow.com", 
            "3. Python Documentation - https://docs.python.org",
            "4. OpenAI API - https://platform.openai.com",
            "5. FastAPI Documentation - https://fastapi.tiangolo.com"
        ],
        "frequent": [
            "1. GitHub (15 visits)",
            "2. Stack Overflow (12 visits)",
            "3. Python Documentation (8 visits)", 
            "4. OpenAI API (6 visits)",
            "5. FastAPI Documentation (4 visits)"
        ],
        "domains": [
            "1. github.com (15 visits)",
            "2. stackoverflow.com (12 visits)",
            "3. docs.python.org (8 visits)",
            "4. platform.openai.com (6 visits)",
            "5. fastapi.tiangolo.com (4 visits)"
        ],
        "search": [
            f"Found {limit} results for '{query}':",
            "1. Python Programming Tutorial - https://python.org/tutorial",
            "2. Python Best Practices - https://docs.python.org/3/tutorial",
            "3. Python Libraries - https://pypi.org"
        ]
    }
    
    data = mock_data.get(analysis_type, mock_data["search"])
    return f"Found {len(data)} history entries:\n\n" + "\n".join(data[:limit])


def _format_history_results(results, analysis_type, query=""):
    """Format history query results for display."""
    if not results:
        return f"No history entries found for query: '{query}'"
    
    if analysis_type == "domains":
        response = f"Top {len(results)} most visited domains:\n\n"
        for i, (domain, visit_count, last_visit) in enumerate(results, 1):
            response += f"{i}. {domain}\n"
            response += f"   Visits: {visit_count}\n"
            response += f"   Last visit: {last_visit}\n\n"
    else:
        response = f"Found {len(results)} history entries"
        if query:
            response += f" matching '{query}'"
        response += ":\n\n"
        
        for i, result in enumerate(results, 1):
            if len(result) == 4:  # url, title, visit_time, visit_count
                url, title, visit_time, visit_count = result
                
                # Truncate long URLs and titles for readability
                display_url = url[:80] + "..." if len(url) > 80 else url
                display_title = title[:60] + "..." if len(title) > 60 else title
                
                response += f"{i}. {display_title}\n"
                response += f"   URL: {display_url}\n"
                response += f"   Visited: {visit_time}\n"
                if visit_count > 1:
                    response += f"   Visit count: {visit_count}\n"
                response += "\n"
    
    return response


@tool
def read_chrome_history(query: str = "", limit: int = 10, analysis_type: str = "search") -> str:
    """Read and analyze Google Chrome browser history with intelligent insights."""
    try:
        # Check if we should use mock data (to avoid security alerts)
        use_mock = os.getenv("USE_MOCK_CHROME_DATA", "false").lower() == "true"
        
        if use_mock:
            return _get_mock_history_data(query, limit, analysis_type)
        
        history_db = _get_chrome_history_path()
        print(f"History DB: {history_db}")
        print(f"Query: {query}")
        print(f"Limit: {limit}")
        print(f"Analysis type: {analysis_type}")
        if not history_db:
            return "Chrome history database not found. Please ensure Chrome is installed and has been used."
        
        # Create temporary copy to avoid conflicts with running Chrome
        temp_db = _create_temp_db_copy(history_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Query the history based on analysis type
        if analysis_type == "recent":
            cursor.execute("""
                SELECT url, title, datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') as visit_time,
                       visit_count
                FROM urls 
                ORDER BY last_visit_time DESC 
                LIMIT ?
            """, (limit,))
        elif analysis_type == "frequent":
            cursor.execute("""
                SELECT url, title, datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') as visit_time,
                       visit_count
                FROM urls 
                WHERE visit_count > 1
                ORDER BY visit_count DESC 
                LIMIT ?
            """, (limit,))
        elif analysis_type == "domains":
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN url LIKE 'https://%' THEN substr(url, 9, instr(substr(url, 9), '/') - 1)
                        WHEN url LIKE 'http://%' THEN substr(url, 8, instr(substr(url, 8), '/') - 1)
                        ELSE 'unknown'
                    END as domain,
                    COUNT(*) as visit_count,
                    MAX(datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch')) as last_visit
                FROM urls 
                GROUP BY domain
                ORDER BY visit_count DESC 
                LIMIT ?
            """, (limit,))
        else:  # search
            if query:
                cursor.execute("""
                    SELECT url, title, datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') as visit_time,
                           visit_count
                    FROM urls 
                    WHERE url LIKE ? OR title LIKE ?
                    ORDER BY last_visit_time DESC 
                    LIMIT ?
                """, (f"%{query}%", f"%{query}%", limit))
            else:
                cursor.execute("""
                    SELECT url, title, datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') as visit_time,
                           visit_count
                    FROM urls 
                    ORDER BY last_visit_time DESC 
                    LIMIT ?
                """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        os.unlink(temp_db)  # Clean up temp file
        
        return _format_history_results(results, analysis_type, query)
        
    except Exception as e:
        return f"Error reading Chrome history: {str(e)}. Make sure Chrome is not running and try again."


@tool
def analyze_browsing_patterns(timeframe: str = "week") -> str:
    """Analyze browsing patterns and provide insights about web usage."""
    try:
        history_db = _get_chrome_history_path()
        if not history_db:
            return "Chrome history database not found. Please ensure Chrome is installed and has been used."
        
        temp_db = _create_temp_db_copy(history_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Calculate time filter based on timeframe
        if timeframe == "day":
            time_filter = "datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') >= datetime('now', '-1 day')"
        elif timeframe == "week":
            time_filter = "datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') >= datetime('now', '-7 days')"
        elif timeframe == "month":
            time_filter = "datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') >= datetime('now', '-30 days')"
        else:
            time_filter = "1=1"  # All time
        
        # Get domain statistics
        cursor.execute(f"""
            SELECT 
                CASE 
                    WHEN url LIKE 'https://%' THEN substr(url, 9, instr(substr(url, 9), '/') - 1)
                    WHEN url LIKE 'http://%' THEN substr(url, 8, instr(substr(url, 8), '/') - 1)
                    ELSE 'unknown'
                END as domain,
                COUNT(*) as visit_count,
                MAX(datetime(last_visit_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch')) as last_visit
            FROM urls 
            WHERE {time_filter}
            GROUP BY domain
            ORDER BY visit_count DESC 
            LIMIT 10
        """)
        
        domain_results = cursor.fetchall()
        
        # Get total visits
        cursor.execute(f"""
            SELECT COUNT(*) as total_visits
            FROM urls 
            WHERE {time_filter}
        """)
        
        total_visits = cursor.fetchone()[0]
        
        conn.close()
        os.unlink(temp_db)
        
        # Format analysis
        response = f"📊 Browsing Analysis for the last {timeframe}:\n\n"
        response += f"Total visits: {total_visits}\n\n"
        response += "Top 10 most visited domains:\n\n"
        
        for i, (domain, visit_count, last_visit) in enumerate(domain_results, 1):
            percentage = (visit_count / total_visits * 100) if total_visits > 0 else 0
            response += f"{i}. {domain}\n"
            response += f"   Visits: {visit_count} ({percentage:.1f}%)\n"
            response += f"   Last visit: {last_visit}\n\n"
        
        return response
        
    except Exception as e:
        return f"Error analyzing browsing patterns: {str(e)}. Make sure Chrome is not running and try again."
