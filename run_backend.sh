#!/bin/bash
# This script activates the Python virtual environment and starts the backend server.
# It's intended to be called by npm/yarn scripts.

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
VENV_PATH="$SCRIPT_DIR/.venv/bin/activate"

if [ -f "$VENV_PATH" ]; then
    echo "BACKEND: Activating Python virtual environment from $VENV_PATH..."
    source "$VENV_PATH"
else
    echo "BACKEND: WARNING - .venv not found or not activated. Backend might not run correctly."
    echo "BACKEND: Please run 'make setup' from the project root first."
    # Optionally, exit 1 here if strict venv enforcement is desired
fi

echo "BACKEND: Starting FastAPI server (ws_server.py)..."
# Default port can be overridden by PORT environment variable
python "$SCRIPT_DIR/ws_server.py" --port "${PORT:-8000}"
