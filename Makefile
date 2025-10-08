# FastAPI Project Makefile

# Variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
APP = main:app
HOST = 0.0.0.0
PORT = 8000

# Default target
.PHONY: help
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Setup commands
.PHONY: setup
setup: ## Create virtual environment and install dependencies
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

.PHONY: install
install: ## Install dependencies
	$(PIP) install -r requirements.txt

.PHONY: install-dev
install-dev: ## Install development dependencies
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-asyncio httpx black isort flake8

# Server commands
.PHONY: run
run: ## Run the FastAPI server
	$(PYTHON) main.py

.PHONY: dev
dev: ## Run the server in development mode with auto-reload
	$(PYTHON) -m uvicorn $(APP) --host $(HOST) --port $(PORT) --reload

.PHONY: prod
prod: ## Run the server in production mode
	$(PYTHON) -m uvicorn $(APP) --host $(HOST) --port $(PORT) --workers 4

# Testing commands
.PHONY: test
test: ## Run tests
	$(PYTHON) -m pytest

.PHONY: test-cov
test-cov: ## Run tests with coverage
	$(PYTHON) -m pytest --cov=.

# Code quality commands
.PHONY: format
format: ## Format code with black and isort
	$(PYTHON) -m black .
	$(PYTHON) -m isort .

.PHONY: lint
lint: ## Lint code with flake8
	$(PYTHON) -m flake8 .

.PHONY: check
check: lint ## Run all code quality checks

# Utility commands
.PHONY: clean
clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete

.PHONY: clean-venv
clean-venv: ## Remove virtual environment
	rm -rf $(VENV_DIR)

.PHONY: reset
reset: clean-venv setup ## Reset project (remove venv and reinstall)

# Health check
.PHONY: health
health: ## Check if server is running
	@curl -s http://localhost:$(PORT)/health || echo "Server is not running"

# Show server info
.PHONY: info
info: ## Show server information
	@echo "FastAPI Server Information:"
	@echo "  URL: http://$(HOST):$(PORT)"
	@echo "  Docs: http://$(HOST):$(PORT)/docs"
	@echo "  ReDoc: http://$(HOST):$(PORT)/redoc"
	@echo "  Health: http://$(HOST):$(PORT)/health"
