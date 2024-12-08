ifneq (,$(wildcard ./.env))
    include .env
    export $(shell sed 's/=.*//' .env)
endif

#ifneq (,$(wildcard ./.env.test))
#    include .env.test
#    export $(shell sed 's/=.*//' .env.test)
#endif

.PHONY: start tests makemigration migrate exportpath cli-createdb cli-dropdb cli-all cli-base lint

start:
	@echo "Starting Uvicorn server (8001)..."
	poetry run uvicorn src.main:app --reload --port 8001

tests:
	@echo "Running tests..."
	poetry run pytest -p no:warnings -v tests/

makemigration:
	@echo "Creating revision..."
	poetry run alembic -c migrations/alembic.ini revision --autogenerate

migrate:
	@echo "Migrating..."
	poetry run alembic -c migrations/alembic.ini upgrade head

exportpath:
	export PYTHONPATH=./src

lint:
	poetry run black ./
	poetry run isort ./
	poetry run ruff check ./
	poetry run mypy ./

# CLI commands for Linux and macOS
cli-createdb:
	poetry run python3 -m src.core.cli.cli create_database

cli-dropdb:
	poetry run python3 -m src.core.cli.cli drop_database

cli-tables:
	poetry run python3 -m src.core.cli.cli create_tables

cli-all:
	poetry run python3 -m src.core.cli.cli bulk_insert_all_jsons

cli-base:
	poetry run python3 -m src.core.cli.cli bulk_insert_base_jsons

# Windows CLI commands
win-cli-createdb:
	poetry run python -m src.core.cli.cli create_database

win-cli-dropdb:
	poetry run python -m src.core.cli.cli drop_database

win-cli-tables:
	poetry run python -m src.core.cli.cli create_tables

win-cli-all:
	poetry run python -m src.core.cli.cli bulk_insert_all_jsons

win-cli-base:
	poetry run python -m src.core.cli.cli bulk_insert_base_jsons
