#!/usr/bin/env python3
"""
Run the agent in safe mode (no Chrome history access, no security alerts).
"""

import os
import sys

# Set environment variable for mock data
os.environ["USE_MOCK_CHROME_DATA"] = "true"

# Import and run the main application
if __name__ == "__main__":
    # Import main after setting environment variable
    from main import app
    import uvicorn
    
    print("🛡️  Running in SAFE MODE (mock data only)")
    print("   - No Chrome history access")
    print("   - No security alerts")
    print("   - Mock data for all tools")
    print("   - Server starting on http://localhost:8000")
    print()
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
