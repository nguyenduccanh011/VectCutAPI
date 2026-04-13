@echo off
REM MCP Server Launcher for Windows
REM Automatically detects python or python3 and runs mcp_server.py

setlocal enabledelayedexpansion

REM Try python3 first, then python
for /f "tokens=*" %%i in ('where python3 2^>nul') do (
    set "PYTHON_CMD=%%i"
    goto :found_python
)

for /f "tokens=*" %%i in ('where python 2^>nul') do (
    set "PYTHON_CMD=%%i"
    goto :found_python
)

echo Error: Python not found in PATH
exit /b 1

:found_python
echo Using Python: !PYTHON_CMD!
cd /d "%~dp0.."
!PYTHON_CMD! mcp_server.py
