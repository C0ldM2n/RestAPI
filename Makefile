ifneq (,$(wildcard ./.env))
    include .env
    export $(shell sed 's/=.*//' .env)
endif

.PHONY: setup requirements start tests makemigration migrate lint cli-createdb cli-dropdb cli-all cli-base

setup:
	@echo "Setting up virtual environment..."
	uv venv
	uv sync

requirements:
	@echo "Compiling project dependencies to requirements.txt..."
	uv pip compile pyproject.toml -o requirements.txt

start:
	@echo "Starting Uvicorn server (8001)..."
	uv run uvicorn src.main:app --reload --port 8001

tests:
	@echo "Running tests..."
	uv run --env-file .env.test pytest -p no:warnings -v ./tests/

makemigration:
	@echo "Creating revision..."
	uv run alembic -c migrations/alembic.ini revision --autogenerate

migrate:
	@echo "Migrating..."
	uv run alembic -c migrations/alembic.ini upgrade head

lint:
	uv tool run black ./
	uv tool run isort ./
	uv tool run mypy ./
	uv tool run ruff check ./

# CLI commands
cli-createdb:
	uv run -m src.core.cli.cli create_database

cli-dropdb:
	uv run -m src.core.cli.cli drop_database

cli-tables:
	uv run -m src.core.cli.cli create_tables

cli-all:
	uv run -m src.core.cli.cli bulk_insert_all_jsons

cli-base:
	uv run -m src.core.cli.cli bulk_insert_base_jsons
