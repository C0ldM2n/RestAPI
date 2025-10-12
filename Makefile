ifneq (,$(wildcard ./.env))
    include .env
    export $(shell sed 's/=.*//' .env)
endif

export PYTHONPATH := src

.PHONY: setup create-requirements start tests create-revision migrate-head lint lint-fix db-create db-drop db-tables db-all db-base

setup:
	@echo "Setting up virtual environment.."
	uv venv
	uv sync

create-requirements:
	@echo "Compiling project dependencies to requirements.txt.."
	uv pip compile pyproject.toml -o requirements.txt

start:
	@echo "Starting Uvicorn server (8001).."
	uv run uvicorn src.main:app --reload --port 8001

tests:
	@echo "Running tests.."
	uv run --env-file .env.test pytest -p no:warnings -v ./tests/

create-revision:
	@echo "Creating revision.."
	uv run alembic revision --autogenerate

migrate-head:
	@echo "Migrating.."
	uv run alembic upgrade head

lint:
	uv tool run ruff check ./src
	uv tool run ruff check ./tests
	uv tool run ruff format ./tests
	uv tool run ruff format ./tests

lint-fix:
	uv tool run ruff check ./src --fix
	uv tool run ruff check ./tests --fix

# DB commands
db-create:
	uv run -m src.core.cli.cli create_database

db-drop:
	uv run -m src.core.cli.cli drop_database

db-tables:
	uv run -m src.core.cli.cli create_tables

db-all:
	uv run -m src.core.cli.cli bulk_insert_all_jsons

db-base:
	uv run -m src.core.cli.cli bulk_insert_base_jsons
