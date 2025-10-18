#!/usr/bin/env python3
"""
Demo script showing file analysis capabilities.
"""

import os
from tools.file_analysis_tool import (
    list_folder_contents,
    read_file_content,
    analyze_folder_structure,
    search_files_in_folder,
    get_file_summary
)

def demo_file_analysis():
    """Demonstrate file analysis capabilities."""
    print("🤖 File Analysis Agent Demo")
    print("=" * 50)
    
    # Demo 1: List folder contents
    print("\n📁 Demo 1: List Folder Contents")
    print("-" * 30)
    result = list_folder_contents.invoke({
        "folder_path": ".",
        "include_hidden": False
    })
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Demo 2: Read a file
    print("\n📄 Demo 2: Read File Content")
    print("-" * 30)
    result = read_file_content.invoke({
        "file_path": "README.md",
        "max_lines": 10
    })
    print(result[:400] + "..." if len(result) > 400 else result)
    
    # Demo 3: Analyze folder structure
    print("\n🔍 Demo 3: Analyze Folder Structure")
    print("-" * 30)
    result = analyze_folder_structure.invoke({
        "folder_path": ".",
        "include_hidden": False
    })
    print(result[:400] + "..." if len(result) > 400 else result)
    
    # Demo 4: Search in files
    print("\n🔍 Demo 4: Search in Files")
    print("-" * 30)
    result = search_files_in_folder.invoke({
        "folder_path": ".",
        "search_term": "FastAPI",
        "file_extensions": "py",
        "case_sensitive": False
    })
    print(result[:400] + "..." if len(result) > 400 else result)
    
    # Demo 5: Get file summary
    print("\n📊 Demo 5: Get File Summary")
    print("-" * 30)
    result = get_file_summary.invoke({
        "file_path": "main.py"
    })
    print(result[:400] + "..." if len(result) > 400 else result)

def show_usage_examples():
    """Show usage examples for the agent."""
    print("\n💡 Usage Examples for the Agent")
    print("=" * 50)
    
    examples = [
        "List the contents of the current directory",
        "Read the main.py file and show me the first 20 lines",
        "Analyze the structure of this project folder",
        "Search for 'def ' in all Python files",
        "Get a summary of the README.md file",
        "Find all files containing 'FastAPI' in this project",
        "Show me the largest files in the tools directory",
        "Read the requirements.txt file",
        "List all Python files in the agent folder",
        "Search for 'import' statements in Python files"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i:2d}. {example}")
    
    print(f"\n🎯 The agent can now help you with:")
    print("   • File and folder exploration")
    print("   • Content reading and analysis")
    print("   • Text search within files")
    print("   • File statistics and summaries")
    print("   • Project structure analysis")
    print("   • Code exploration and understanding")

if __name__ == "__main__":
    demo_file_analysis()
    show_usage_examples()
    
    print(f"\n✅ File Analysis Agent is ready!")
    print(f"🚀 Start the server with: python main.py")
    print(f"🛡️  Or use safe mode: python run_safe.py")
