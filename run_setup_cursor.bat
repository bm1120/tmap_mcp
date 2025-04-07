@echo off
echo Running Tmap MCP Setup for Cursor Editor...

rem Run the setup script
python %~dp0\setup_cursor.py

echo.
echo Setup completed. Press any key to exit.
pause 