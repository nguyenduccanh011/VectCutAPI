@echo off
REM MCP Server Launcher for Windows - Enhanced
REM Automatically detects python or python3 and runs mcp_server.py

setlocal enabledelayedexpansion

REM Get workspace folder from VS Code argument if provided
if not "%1"=="" (
    set "WORKSPACE_DIR=%1"
) else (
    REM Fallback: use current script's parent directory
    cd /d "%~dp0.."
    for /f "delims=" %%A in ('cd') do set "WORKSPACE_DIR=%%A"
)

REM Try python3 first, then python
for /f "tokens=*" %%i in ('where python3 2^>nul') do (
    set "PYTHON_CMD=%%i"
    goto :found_python
)

for /f "tokens=*" %%i in ('where python 2^>nul') do (
    set "PYTHON_CMD=%%i"
    goto :found_python
)

REM Try checking in common locations
if exist "%PROGRAMFILES%\Python312\python.exe" (
    set "PYTHON_CMD=%PROGRAMFILES%\Python312\python.exe"
    goto :found_python
)

if exist "%PROGRAMFILES%\Python311\python.exe" (
    set "PYTHON_CMD=%PROGRAMFILES%\Python311\python.exe"
    goto :found_python
)

if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    goto :found_python
)

echo Error: Python not found in PATH or common locations
exit /b 2

:found_python
if not exist "%WORKSPACE_DIR%\mcp_server.py" (
    echo Error: mcp_server.py not found at %WORKSPACE_DIR%
    exit /b 2
)

cd /d "%WORKSPACE_DIR%"
set "PYTHONPATH=%WORKSPACE_DIR%"
"%PYTHON_CMD%" mcp_server.py
exit /b %ERRORLEVEL%
