@echo off
setlocal enabledelayedexpansion

echo ======================================================================
echo   PralaySense AI / SAHYADRUSHTI AI - Portable Setup & Launcher
echo ======================================================================

:: 1. Check Python
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

:: 2. Check Node / npm
npm --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Node.js / npm is not installed or not in PATH.
    echo Please install Node.js (v18+) from https://nodejs.org/
    pause
    exit /b 1
)

:: 3. Setup Virtual Environment & Python dependencies
if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Creating Python virtual environment in .venv...
    python -m venv .venv
    echo [INFO] Installing Python requirements...
    .venv\Scripts\pip install -r requirements.txt
) else (
    echo [OK] Virtual environment detected.
)

:: 4. Setup Frontend node_modules
if not exist "frontend\node_modules" (
    echo [INFO] Installing frontend packages (npm install)...
    cd frontend
    call npm install
    cd ..
) else (
    echo [OK] Frontend node_modules detected.
)

:: 5. Launch Application using PowerShell starter
echo [INFO] Launching backend and frontend...
powershell -ExecutionPolicy Bypass -File scripts\start_demo.ps1

pause
