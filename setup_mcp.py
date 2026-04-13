#!/usr/bin/env python3
"""
Setup script for MCP configuration based on OS
Automatically configures .vscode/mcp.json for your platform
"""

import os
import sys
import json
import platform

def setup_mcp_config():
    """Configure MCP based on current OS"""
    
    vscode_dir = os.path.join(os.path.dirname(__file__), '.vscode')
    mcp_json_path = os.path.join(vscode_dir, 'mcp.json')
    
    # Determine OS
    current_os = platform.system()
    print(f"Detected OS: {current_os}")
    
    # Config based on OS
    if current_os == 'Windows':
        config = {
            "servers": {
                "capcut-api": {
                    "type": "stdio",
                    "command": ".vscode/run-mcp.cmd",
                    "cwd": "${workspaceFolder}",
                    "env": {
                        "PYTHONPATH": "${workspaceFolder}"
                    }
                }
            }
        }
        print("✅ Configured for Windows (using run-mcp.cmd)")
    else:
        # macOS, Linux, etc.
        config = {
            "servers": {
                "capcut-api": {
                    "type": "stdio",
                    "command": ".vscode/run-mcp.sh",
                    "cwd": "${workspaceFolder}",
                    "env": {
                        "PYTHONPATH": "${workspaceFolder}"
                    }
                }
            }
        }
        
        # Make shell script executable
        run_mcp_sh = os.path.join(vscode_dir, 'run-mcp.sh')
        if os.path.exists(run_mcp_sh):
            os.chmod(run_mcp_sh, 0o755)
            print(f"✅ Made {run_mcp_sh} executable")
        
        print(f"✅ Configured for {current_os} (using run-mcp.sh)")
    
    # Write config
    with open(mcp_json_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Wrote configuration to: {mcp_json_path}")
    print("\nNext steps:")
    print("1. Reload VS Code")
    print("2. Test MCP server in Chat view (Ctrl+Alt+I)")
    print("3. Run 'MCP: List Servers' to check status")
    
    return True

if __name__ == '__main__':
    try:
        setup_mcp_config()
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
