.PHONY: all check-reqs setup-backend setup-frontend build-frontend setup-env setup clean

all: setup

setup: check-reqs setup-backend setup-frontend setup-env
	@echo "----------------------------------------------------------------------"
	@echo "Setup complete! Please review the messages above."
	@echo "Remember to activate your Python virtual environment: source .venv/bin/activate"
	@echo "And configure your .env.production and frontend/.env.local files."
	@echo "----------------------------------------------------------------------"

check-reqs:
	@echo ">>> Checking system requirements..."
	@if ! python3 --version 2>&1 | grep -qE "3\.(1[0-9]|[2-9][0-9])"; then \
		echo "Error: Python 3.10+ is required. Please install or update Python."; \
		exit 1; \
	fi
	@echo "Python version check: OK (found $(shell python3 --version))"
	@if ! node --version 2>&1 | grep -qE "v(18|[2-9][0-9])\."; then \
		echo "Error: Node.js v18+ is required. Please install or update Node.js."; \
		exit 1; \
	fi
	@echo "Node.js version check: OK (found $(shell node --version))"
	@if ! yarn --version > /dev/null 2>&1; then \
		echo "Error: Yarn is required. Please install Yarn."; \
		exit 1; \
	fi
	@echo "Yarn installation check: OK (found $(shell yarn --version))"
	@echo "System requirements check passed."

setup-backend:
	@echo ">>> Setting up backend..."
	@echo "Ensuring you are in the project root directory."
	@if [ ! -f "pyproject.toml" ]; then \
		echo "Error: pyproject.toml not found. Make sure you are in the project root directory."; \
		exit 1; \
	fi
	@if [ ! -d ".venv" ]; then \
		echo "Creating Python virtual environment (.venv)..."; \
		python3 -m venv .venv; \
	else \
		echo "Python virtual environment (.venv) already exists."; \
	fi
	@echo "To activate the virtual environment, run: source .venv/bin/activate (Linux/macOS) or .\\.venv\\Scripts\\activate (Windows)"; \
	@echo "Installing backend dependencies (pip install .)..."; \
	./.venv/bin/pip install .
	@echo "Backend setup complete."

setup-frontend:
	@echo ">>> Setting up frontend..."
	@echo "Navigating to frontend directory..."
	cd frontend && \
	echo "Installing frontend dependencies (yarn install)..." && \
	yarn install && \
	echo "Navigating back to project root..." && \
	cd ..
	@echo "Frontend setup complete."

build-frontend:
	@echo ">>> Building frontend..."
	@echo "Navigating to frontend directory..."
	cd frontend && \
	echo "Building frontend (yarn build)..." && \
	yarn build && \
	echo "Navigating back to project root..." && \
	cd ..
	@echo "Frontend build complete."

setup-env:
	@echo ">>> Setting up environment files..."
	@if [ ! -f "frontend/.env.local" ] && [ -f "frontend/.env.example" ]; then \
		echo "Copying frontend/.env.example to frontend/.env.local..."; \
		cp frontend/.env.example frontend/.env.local; \
		echo "Please customize frontend/.env.local with your settings (e.g., NEXT_PUBLIC_API_URL)."; \
	elif [ -f "frontend/.env.local" ]; then \
		echo "frontend/.env.local already exists. Please ensure it is configured correctly."; \
	else \
		echo "Warning: frontend/.env.example not found. Cannot create frontend/.env.local."; \
	fi
	@echo "Please ensure .env.production (in the project root) is configured with your backend API keys."
	@echo "Refer to .env.production.example for guidance."
	@echo "Key variables include: OPENROUTER_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY."
	@echo "Environment file setup guidance complete."

clean:
	@echo ">>> Cleaning up project..."
	rm -rf .venv
	rm -rf frontend/node_modules
	rm -rf frontend/.next
	rm -rf build dist *.egg-info
	@echo "Cleanup complete."
