<#
.SYNOPSIS
    PralaySense AI / SAHYADRUSHTI AI - One-Click Demo Launcher
.DESCRIPTION
    Starts the FastAPI backend and Vite frontend development servers for live evaluation.
#>

$ErrorActionPreference = "Stop"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  PralaySense AI (सह्यादृष्टी) - Local Evaluation & Demo Environment" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# 1. Check Python virtual environment
$PythonExe = "python"
if (Test-Path ".\.venv\Scripts\python.exe") {
    $PythonExe = ".\.venv\Scripts\python.exe"
    Write-Host "[OK] Using virtual environment Python: $PythonExe" -ForegroundColor Green
} else {
    Write-Host "[INFO] Using system Python: $PythonExe" -ForegroundColor Yellow
}

# 1b. Ensure .env exists with a secure random JWT_SECRET if not already present
if (-not (Test-Path ".\.env")) {
    Write-Host "[INFO] No .env file detected. Generating .env with secure random JWT secret..." -ForegroundColor Yellow
    Copy-Item ".\.env.example" ".\.env"
    $randSecret = & $PythonExe -c "import secrets; print(secrets.token_urlsafe(48))"
    (Get-Content ".\.env") -replace 'JWT_SECRET=".*"', "JWT_SECRET=`"$randSecret`"" | Set-Content ".\.env"
    Write-Host "[OK] Generated .env file with randomized session secret." -ForegroundColor Green
}

# 2. Run automated sanity check harness
Write-Host "`n[1/3] Running problem statement validation harness (ps_check.py)..." -ForegroundColor Yellow
& $PythonExe scripts/ps_check.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARNING] ps_check harness reported non-zero status. Proceeding in demo mode." -ForegroundColor Magenta
}

# 3. Start Backend Server in a new window
Write-Host "`n[2/3] Starting FastAPI Backend on http://127.0.0.1:8000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$PythonExe' -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

# 4. Start Frontend Client in a new window
Write-Host "`n[3/3] Starting Vite Frontend on http://localhost:5173..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cmd /c 'npm --prefix frontend run dev'"

Write-Host "`n======================================================================" -ForegroundColor Green
Write-Host "  Servers launched successfully!" -ForegroundColor Green
Write-Host "  - Frontend UI:  http://localhost:5173" -ForegroundColor Cyan
Write-Host "  - Backend API: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host "  - Demo Script: docs/DEMO_SCRIPT.md" -ForegroundColor Cyan
Write-Host "======================================================================`n" -ForegroundColor Green

