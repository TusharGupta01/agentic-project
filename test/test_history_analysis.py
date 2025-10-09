#!/usr/bin/env python3
"""
Test script for the enhanced browsing history analysis capabilities.
"""

import os
import sys
sys.path.append('..')
from agent import read_chrome_history, analyze_browsing_patterns

def test_history_analysis():
    """Test the enhanced Chrome history analysis tools."""
    print("🔍 Testing Enhanced Browsing History Analysis")
    print("=" * 60)
    
    # Test 1: Recent history
    print("\n📋 Test 1: Recent browsing history")
    try:
        result = read_chrome_history.invoke({"query": "", "limit": 5, "analysis_type": "recent"})
        print(f"Result: {result[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Frequent sites
    print("\n🔄 Test 2: Most frequently visited sites")
    try:
        result = read_chrome_history.invoke({"query": "", "limit": 5, "analysis_type": "frequent"})
        print(f"Result: {result[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Domain analysis
    print("\n🌐 Test 3: Top domains by visit count")
    try:
        result = read_chrome_history.invoke({"query": "", "limit": 5, "analysis_type": "domains"})
        print(f"Result: {result[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Search functionality
    print("\n🔍 Test 4: Search for 'github' in history")
    try:
        result = read_chrome_history.invoke({"query": "github", "limit": 3, "analysis_type": "search"})
        print(f"Result: {result[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 5: Browsing pattern analysis
    print("\n📊 Test 5: Browsing pattern analysis (last week)")
    try:
        result = analyze_browsing_patterns.invoke({"timeframe": "week"})
        print(f"Result: {result[:300]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 6: Daily analysis
    print("\n📅 Test 6: Daily browsing analysis")
    try:
        result = analyze_browsing_patterns.invoke({"timeframe": "day"})
        print(f"Result: {result[:200]}...")
    except Exception as e:
        print(f"Error: {e}")

def show_usage_examples():
    """Show usage examples for the enhanced history analysis."""
    print("\n📖 Enhanced Usage Examples")
    print("=" * 60)
    print("The enhanced agent can now help you with:")
    print()
    print("🔍 **History Analysis Types:**")
    print("• Recent browsing history")
    print("• Most frequently visited sites")
    print("• Top domains by visit count")
    print("• Keyword search through history")
    print()
    print("📊 **Pattern Analysis:**")
    print("• Daily browsing patterns")
    print("• Weekly browsing trends")
    print("• Monthly usage statistics")
    print("• Domain popularity analysis")
    print()
    print("💬 **Example Queries:**")
    print('• "Show me my recent browsing history"')
    print('• "What are my most visited websites?"')
    print('• "Analyze my browsing patterns for the last week"')
    print('• "Find websites about machine learning"')
    print('• "Which domains do I visit most frequently?"')
    print('• "What GitHub repositories have I visited?"')
    print('• "Show me my YouTube watch history"')

if __name__ == "__main__":
    print("🤖 Enhanced Browsing History Analysis Test Suite")
    print("=" * 60)
    
    test_history_analysis()
    show_usage_examples()
    
    print("\n✅ Enhanced history analysis testing completed!")
    print("\nThe agent is now specialized for browsing history analysis")
    print("and can provide deep insights into your web usage patterns.")
