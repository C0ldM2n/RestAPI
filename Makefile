ifneq (,$(wildcard ./.env))
    include .env
    export $(shell sed 's/=.*//' .env)
endif

#ifneq (,$(wildcard ./.env.test))
#    include .env.test
#    export $(shell sed 's/=.*//' .env.test)
#endif

.PHONY: start tests makemigration migrate exportpath cli-createdb cli-dropdb cli-all cli-base

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


cli-createdb:
	poetry run python3 -m src.core.cli.cli create_database
#		Maybe create revision and migration after creating db and tables?

cli-dropdb:
	poetry run python3 -m src.core.cli.cli drop_database

cli-tables:
	poetry run python3 -m src.core.cli.cli create_tables

cli-all:
	poetry run python3 -m src.core.cli.cli bulk_insert_all_jsons

cli-base:
	poetry run python3 -m src.core.cli.cli bulk_insert_base_jsons