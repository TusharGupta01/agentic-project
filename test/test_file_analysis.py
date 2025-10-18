#!/usr/bin/env python3
"""
Test script for file analysis functionality.
"""

import sys
sys.path.append('..')
from tools.file_analysis_tool import (
    list_folder_contents,
    read_file_content,
    analyze_folder_structure,
    search_files_in_folder,
    get_file_summary
)

def test_list_folder():
    """Test listing folder contents."""
    print("📁 Testing list_folder_contents")
    print("=" * 40)
    
    # Test with current directory
    result = list_folder_contents.invoke({
        "folder_path": ".",
        "include_hidden": False,
        "max_depth": 1
    })
    print(result[:300] + "..." if len(result) > 300 else result)

def test_read_file():
    """Test reading file content."""
    print("\n📄 Testing read_file_content")
    print("=" * 40)
    
    # Test with a known file
    result = read_file_content.invoke({
        "file_path": "main.py",
        "max_lines": 20
    })
    print(result[:400] + "..." if len(result) > 400 else result)

def test_analyze_folder():
    """Test folder structure analysis."""
    print("\n🔍 Testing analyze_folder_structure")
    print("=" * 40)
    
    result = analyze_folder_structure.invoke({
        "folder_path": ".",
        "include_hidden": False
    })
    print(result[:400] + "..." if len(result) > 400 else result)

def test_search_files():
    """Test searching files."""
    print("\n🔍 Testing search_files_in_folder")
    print("=" * 40)
    
    result = search_files_in_folder.invoke({
        "folder_path": ".",
        "search_term": "def ",
        "file_extensions": "py",
        "case_sensitive": False
    })
    print(result[:400] + "..." if len(result) > 400 else result)

def test_file_summary():
    """Test file summary."""
    print("\n📊 Testing get_file_summary")
    print("=" * 40)
    
    result = get_file_summary.invoke({
        "file_path": "main.py"
    })
    print(result[:400] + "..." if len(result) > 400 else result)

def test_agent_integration():
    """Test the agent with file analysis."""
    print("\n🤖 Testing Agent Integration")
    print("=" * 40)
    
    from agent.workflow import run_agent
    from agent.memory import conversation_memory
    
    # Create a session
    session_id = conversation_memory.create_session()
    
    # Test queries
    queries = [
        "List the contents of the current directory",
        "Read the main.py file",
        "Analyze the structure of this project folder",
        "Search for 'def ' in Python files"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        try:
            result = run_agent(query, session_id)
            print(f"Response: {result[:200]}...")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("🧪 File Analysis Test Suite")
    print("=" * 50)
    
    try:
        test_list_folder()
        test_read_file()
        test_analyze_folder()
        test_search_files()
        test_file_summary()
        test_agent_integration()
        
        print("\n✅ All file analysis tests completed!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
