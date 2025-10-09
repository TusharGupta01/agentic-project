"""
Main agent module - simplified entry point for the browsing history analysis agent.
"""

from agent import run_agent, create_agent_graph, AgentState

# Initialize the agent
agent_app = create_agent_graph()

# Example usage
if __name__ == "__main__":
    # Test the agent
    test_queries = [
        "What are my most visited websites?",
        "Show me my recent browsing history",
        "Find websites about Python programming",
        "Analyze my browsing patterns for the last week"
    ]
    
    for query in test_queries:
        print(f"\nUser: {query}")
        response = run_agent(query)
        print(f"Agent: {response}")
