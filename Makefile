.PHONY: help install install-dev lint format typecheck test test-backend test-bot test-worker clean docker-build docker-up docker-down migrate docs

help:
	@echo "QuantX AI Development Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install        - Install production dependencies"
	@echo "  install-dev    - Install development dependencies"
	@echo "  lint           - Run linters (ruff, black, isort)"
	@echo "  format         - Auto-format code"
	@echo "  typecheck      - Run type checkers (mypy)"
	@echo "  test           - Run all tests with coverage"
	@echo "  test-backend   - Run backend tests"
	@echo "  test-bot       - Run bot tests"
	@echo "  test-worker    - Run worker tests"
	@echo "  clean          - Clean build artifacts and caches"
	@echo "  docker-build   - Build Docker images"
	@echo "  docker-up      - Start development environment"
	@echo "  docker-down    - Stop development environment"
	@echo "  migrate        - Run database migrations"
	@echo "  docs           - Build documentation"

install:
	@echo "Installing dependencies..."
	pip install -e backend
	pip install -e bot
	pip install -e worker
	pip install -e shared/python

install-dev:
	@echo "Installing development dependencies..."
	install
	pip install pytest pytest-asyncio pytest-cov coverage
	pip install ruff black isort mypy

lint:
	@echo "Running linters..."
	ruff check backend/src bot/src worker/src shared/python
	black --check backend/src bot/src worker/src shared/python
	isort --check-only backend/src bot/src worker/src shared/python

format:
	@echo "Formatting code..."
	ruff check --fix backend/src bot/src worker/src shared/python
	black backend/src bot/src worker/src shared/python
	isort backend/src bot/src worker/src shared/python

typecheck:
	@echo "Running type checkers..."
	mypy backend/src bot/src worker/src shared/python

test:
	@echo "Running all tests..."
	pytest tests backend/tests bot/tests worker/tests --cov=backend/src --cov=bot/src --cov=worker/src --cov=shared/python --cov-report=term-missing

test-backend:
	@echo "Running backend tests..."
	pytest backend/tests --cov=backend/src --cov-report=term-missing

test-bot:
	@echo "Running bot tests..."
	pytest bot/tests --cov=bot/src --cov-report=term-missing

test-worker:
	@echo "Running worker tests..."
	pytest worker/tests --cov=worker/src --cov-report=term-missing

clean:
	@echo "Cleaning artifacts..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache .coverage htmlcov dist build .eggs

docker-build:
	@echo "Building Docker images..."
	docker build -t quantx-api:dev ./backend
	docker build -t quantx-bot:dev ./bot
	docker build -t quantx-worker:dev ./worker

docker-up:
	@echo "Starting development environment..."
	docker-compose up -d

docker-down:
	@echo "Stopping development environment..."
	docker-compose down

migrate:
	@echo "Running database migrations..."
	cd backend && alembic upgrade head

docs:
	@echo "Building documentation..."
	mkdocs serve
