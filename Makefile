# GOK:AI Makefile
# Convenience commands for development and deployment

.PHONY: help install dev test docker docker-build docker-up docker-down clean lint format

# Default target
help:
	@echo "GOK:AI Development Commands"
	@echo "=============================="
	@echo ""
	@echo "Development:"
	@echo "  make install        - Install dependencies in virtual environment"
	@echo "  make dev            - Setup development environment"
	@echo "  make run            - Run main application"
	@echo ""
	@echo "Testing:"
	@echo "  make test           - Run test suite"
	@echo "  make test-cov       - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint           - Run linters (flake8, mypy)"
	@echo "  make format         - Format code (black, isort)"
	@echo "  make clean          - Remove build artifacts and cache"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build   - Build Docker images"
	@echo "  make docker-up      - Start Docker Compose stack"
	@echo "  make docker-down    - Stop Docker Compose stack"
	@echo "  make docker-logs    - View Docker Compose logs"
	@echo ""
	@echo "Infrastructure:"
	@echo "  make shell          - Open interactive Python shell"
	@echo "  make db-migrate     - Run database migrations"
	@echo ""

# Setup and Installation
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@if [ -f "MTAQUEST/requirements.txt" ]; then \
		echo "Installing MTAQUEST dependencies..."; \
		pip install -r MTAQUEST/requirements.txt; \
	fi

dev:
	@echo "Setting up development environment..."
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
		echo "Virtual environment created"; \
	fi
	@if [ -f "setup-dev.sh" ]; then \
		bash setup-dev.sh; \
	elif [ -f "setup-dev.bat" ]; then \
		cmd /c setup-dev.bat; \
	fi

run:
	@echo "Starting GOK:AI application..."
	python main.py

# Testing
test:
	@echo "Running test suite..."
	pytest tests/ -v

test-cov:
	@echo "Running tests with coverage..."
	pytest tests/ --cov=CORE --cov=INFRA --cov=MTAQUEST --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

# Code Quality
lint:
	@echo "Running linters..."
	flake8 CORE INFRA MTAQUEST ECONOMY META PERCEPTION --max-line-length=120
	mypy CORE INFRA --ignore-missing-imports

format:
	@echo "Formatting code..."
	black CORE INFRA MTAQUEST ECONOMY META PERCEPTION tests
	isort CORE INFRA MTAQUEST ECONOMY META PERCEPTION tests
	@echo "Code formatted successfully"

clean:
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ htmlcov/ .coverage .pytest_cache/
	@echo "Cleanup complete"

# Docker Operations
docker-build:
	@echo "Building Docker images..."
	docker-compose build
	@echo "Images built successfully"

docker-up:
	@echo "Starting Docker Compose stack..."
	docker-compose up -d
	@echo "Stack started. Check with: docker-compose ps"

docker-down:
	@echo "Stopping Docker Compose stack..."
	docker-compose down
	@echo "Stack stopped"

docker-logs:
	@echo "Displaying Docker Compose logs..."
	docker-compose logs -f

docker-ps:
	@echo "Docker Compose services status:"
	docker-compose ps

# Interactive Tools
shell:
	@echo "Opening Python shell with GOK:AI context..."
	python -c "import sys; sys.path.insert(0, '.'); from CORE.spiral_pipeline import *; from INFRA.Services.api_server import *; print('GOK:AI context loaded'); import IPython; IPython.embed()" || python

# Database
db-migrate:
	@echo "Running database migrations..."
	python -m CORE.Memory.bootstrap

# Documentation
docs:
	@echo "Generating documentation..."
	python -c "print('Documentation generation not yet implemented')"

.DEFAULT_GOAL := help
