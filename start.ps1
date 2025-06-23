$workspacePath = Join-Path $PSScriptRoot 'workspace'
if (-not (Test-Path $workspacePath)) {
    New-Item -ItemType Directory -Path $workspacePath | Out-Null
    Write-Host "Created workspace directory"
}

$env:FRONTEND_PORT = '3000'
$env:BACKEND_PORT = '8000'
$env:WORKSPACE_PATH = $workspacePath
$env:COMPOSE_PROJECT_NAME = 'agent'

docker compose -f docker/docker-compose.yaml up @args
