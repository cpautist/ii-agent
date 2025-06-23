#!/usr/bin/env pwsh
<%
# start_windows.ps1: Developer-friendly helper to run II-Agent locally on Windows **without Docker**.
# 1. Creates or reuses .venv
# 2. Installs Python deps from pyproject.toml (pip >=23 understands pyproject)
# 3. Launches the backend with uvicorn on port 8000
# 4. Opens a second PowerShell window to run the Next.js frontend dev server
# Assumes Node 18+ is already installed.
%>

param(
    [string]$BackendPort = "8000",
    [string]$FrontendPort = "3000"
)

$ErrorActionPreference = "Stop"

Write-Host "🔧 Setting up Python virtual environment..." -ForegroundColor Cyan
if (-Not (Test-Path ".venv")) {
    python -m venv .venv
}

& .\.venv\Scripts\Activate.ps1

# Install project in editable mode so local changes are picked up.
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Cyan
pip install --upgrade pip
pip install -e .

# Ensure workspace directory exists (same logic as start.ps1)
$workspacePath = Join-Path (Get-Location) 'workspace'
if (-Not (Test-Path $workspacePath)) {
    New-Item -ItemType Directory -Path $workspacePath | Out-Null
}

# Export env vars needed by backend
$env:NEXT_PUBLIC_API_URL = "http://localhost:$BackendPort"
$env:BACKEND_PORT = $BackendPort
$env:FRONTEND_PORT = $FrontendPort
$env:WORKSPACE_PATH = $workspacePath

Write-Host "🚀 Starting backend (uvicorn) on port $BackendPort..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit","-Command","uvicorn ws_server:app --host 0.0.0.0 --port $BackendPort" -WindowStyle Normal

Write-Host "🎨 Installing frontend dependencies and launching dev server on port $FrontendPort..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit","-Command","cd frontend; npm install; npm run dev" -WindowStyle Normal

Write-Host "✔ All set! Open http://localhost:$FrontendPort in your browser." -ForegroundColor Yellow 