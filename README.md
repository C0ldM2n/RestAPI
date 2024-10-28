# REST API | Python 3.12, FastAPI, SQLAlchemy, Pydantic and Poetry
Writing API for the future project. Creating CRUD-operations, routers for them 
and testing all the functionality with pytest (and asyncio).

## Usage
**Required:**
* confgured .env file (for tests .env.test)
* Postgres database
* and use make commands

### Makefile commands:
    make start
Starting Uvicorn server with --reload and on port 8001

    make tests
Running tests from /tests folder

    make makemigration
Creating a database revision

    make migrate
Upgrading to head revision

#### CLI commands
    make cli-createdb
Creating database

    make cli-dropdb
Drop database

    make cli-tables
Creating tables in database

    make cli-all
Inserting all jsons from /data folder

    make cli-base
Inserting base jsons (configured in /src/core/cli/utils.py) from /data folder

## Library versions
Python 3.12.7\
fastapi 0.115.0\
alembic 1.13.2\
sqlalchemy 2.0.35\
pydantic 2.9.2

pytest 8.3.3\
pytest-asyncio 0.24.0
