@echo off
REM PharmaQMS Build Script
REM Run from project root: F:\pangu\data\qa\AutoQA\PharmaQMS\
REM Requires: pnpm (for frontend), .venv already created with requirements installed

setlocal
set PROJECT_DIR=%~dp0..
cd /d "%PROJECT_DIR%"

echo === Step 1: Build frontend ===
cd frontend
call pnpm run build
if errorlevel 1 (echo FAILED: frontend build & exit /b 1)
cd ..

echo === Step 2: PyInstaller bundle ===
REM IMPORTANT: Must use project venv's Python so all deps are included
.venv\Scripts\python.exe -m PyInstaller build\pharma_qms.spec --clean --noconfirm
if errorlevel 1 (echo FAILED: PyInstaller & exit /b 1)

echo === Step 3: Done ===
echo Bundle at: dist\PharmaQMS\
echo Run: dist\PharmaQMS\PharmaQMS.exe
echo.
echo To create installer: run Inno Setup on build\installer.iss
