@echo off
taskkill /F /IM PharmaQMS.exe 2>nul
echo PharmaQMS stopped.
timeout /t 2 /nobreak >nul
