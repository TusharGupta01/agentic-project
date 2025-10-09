#!/usr/bin/env python3
"""
Test script for the Chrome History tool.
This tests the Chrome history reading functionality.
"""

import os
import sys
sys.path.append('..')
from agent import read_chrome_history

def test_chrome_history():
    """Test the Chrome history reading tool."""
    print("🌐 Testing Chrome History Tool")
    print("=" * 50)
    
    # Test 1: Get recent history
    print("\n📋 Test 1: Getting recent history (last 5 entries)")
    try:
        result = read_chrome_history.invoke({"query": "", "limit": 5})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Search for specific terms
    print("\n🔍 Test 2: Searching for 'github' in history")
    try:
        result = read_chrome_history.invoke({"query": "github", "limit": 3})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Search for another term
    print("\n🔍 Test 3: Searching for 'stackoverflow' in history")
    try:
        result = read_chrome_history.invoke({"query": "stackoverflow", "limit": 3})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Search for a domain
    print("\n🔍 Test 4: Searching for 'youtube.com' in history")
    try:
        result = read_chrome_history.invoke({"query": "youtube.com", "limit": 3})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

def check_chrome_installation():
    """Check if Chrome is installed and accessible."""
    print("\n🔍 Checking Chrome Installation")
    print("=" * 50)
    
    # Common Chrome history database locations
    chrome_paths = [
        os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/History"),
        os.path.expanduser("~/AppData/Local/Google/Chrome/User Data/Default/History"),
        os.path.expanduser("~/.config/google-chrome/Default/History"),
        os.path.expanduser("~/snap/chromium/common/chromium/Default/History")
    ]
    
    found_paths = []
    for path in chrome_paths:
        if os.path.exists(path):
            found_paths.append(path)
            print(f"✅ Found Chrome history at: {path}")
        else:
            print(f"❌ Not found: {path}")
    
    if not found_paths:
        print("\n⚠️  Chrome history database not found!")
        print("Make sure Google Chrome is installed and has been used.")
        print("The tool will work once Chrome is installed and has browsing history.")
    else:
        print(f"\n✅ Chrome history database found at {len(found_paths)} location(s)")

def show_usage_examples():
    """Show usage examples for the Chrome history tool."""
    print("\n📖 Usage Examples")
    print("=" * 50)
    print("You can use the Chrome history tool in these ways:")
    print()
    print("1. Get recent browsing history:")
    print('   "Show me my recent browsing history"')
    print('   "What websites have I visited recently?"')
    print()
    print("2. Search for specific websites:")
    print('   "Find websites about Python programming"')
    print('   "Show me my GitHub visits"')
    print('   "What YouTube videos have I watched?"')
    print()
    print("3. Search by domain:")
    print('   "Show me all visits to stackoverflow.com"')
    print('   "Find my visits to reddit.com"')
    print()
    print("4. Search by topic:")
    print('   "Find websites about machine learning"')
    print('   "Show me my research on FastAPI"')

if __name__ == "__main__":
    print("🔍 Chrome History Tool Test Suite")
    print("=" * 50)
    
    check_chrome_installation()
    test_chrome_history()
    show_usage_examples()
    
    print("\n✅ Chrome history tool testing completed!")
    print("\nNote: Chrome must be closed for the tool to work properly.")
    print("The tool creates a temporary copy of the history database to avoid conflicts.")
