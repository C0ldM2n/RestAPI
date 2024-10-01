ifneq (,$(wildcard .env))
    include .env
    export $(shell sed 's/=.*//' .env)
endif

.PHONY: start test makemigrations migrate exportpath cli

start:
    poetry run: uvicorn src.main\:app --reload --port 8001

test:
    poetry run: pytest -p no\:warnings -v tests/

makemigrations:
    poetry run: alembic -c migrations/alembic.ini revision --autogenerate

migrate:
    poetry run: alembic -c migrations/alembic.ini upgrade head

exportpath:
    poetry run: export PYTHONPATH=./src

cli:
    poetry run: python3 -m src.core.cli.cli bulk_insert_base