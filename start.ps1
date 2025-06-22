#!/usr/bin/env pwsh
# Create workspace directory if it doesn't exist
$workspacePath = Join-Path (Get-Location) 'workspace'
if (-not (Test-Path $workspacePath)) {
    New-Item -ItemType Directory -Path $workspacePath | Out-Null
    Write-Host "Created workspace directory"
}

# BACKEND ENVIRONMENT VARIABLES
$env:FRONTEND_PORT = "3000"
$env:BACKEND_PORT = "8000"
$env:WORKSPACE_PATH = $workspacePath

# Start docker-compose with the HOST_IP variable
$env:COMPOSE_PROJECT_NAME = "agent"
docker compose -f "docker/docker-compose.yaml" up $args
