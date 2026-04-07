@echo off
cd /d "%~dp0\.."
start "" /B backend\PharmaQMS.exe
echo Starting PharmaQMS...
timeout /t 3 /nobreak >nul
start http://localhost:8889
echo PharmaQMS is running. Close this window to keep the service running.
echo To stop: run stop.bat or close this window.
pause >nul
