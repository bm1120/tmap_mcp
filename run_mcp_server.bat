@echo off
echo Starting Tmap MCP Server...

rem Set environment variables if not already set
if "%TMAP_APP_KEY%"=="" (
    echo TMAP_APP_KEY environment variable is not set.
    echo Please set your Tmap API key:
    set /p TMAP_APP_KEY="Enter your Tmap API key: "
)

rem Add current directory to Python path
set PYTHONPATH=%PYTHONPATH%;%~dp0

rem Run the MCP server
python %~dp0\mcp_server.py

pause 