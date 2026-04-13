#!/bin/bash
# MCP Server Launcher for Unix/Linux/macOS
# Automatically detects python or python3 and runs mcp_server.py

# Try python3 first, then python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python not found in PATH"
    exit 1
fi

echo "Using Python: $PYTHON_CMD"

# Change to workspace root (parent of .vscode)
cd "$(dirname "$(dirname "${BASH_SOURCE[0]}")")"

# Run mcp_server
"$PYTHON_CMD" mcp_server.py
