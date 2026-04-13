#!/usr/bin/env python3
"""
MCP Server Launcher - Automatically detects and runs mcp_server.py
Works on any machine regardless of python/python3 command availability
"""

import sys
import os
import subprocess

# Get the workspace root (parent directory of .vscode)
workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add workspace root to Python path
sys.path.insert(0, workspace_root)

# Change to workspace directory
os.chdir(workspace_root)

# Import and run mcp_server
try:
    import mcp_server
    # Run the main() function if it exists
    if hasattr(mcp_server, 'main'):
        mcp_server.main()
    else:
        # Otherwise just import should trigger initialization
        pass
except Exception as e:
    print(f"Error running MCP server: {e}", file=sys.stderr)
    sys.exit(1)
