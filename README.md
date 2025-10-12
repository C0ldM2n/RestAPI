# REST API | Python 3.12, FastAPI, SQLAlchemy, Pydantic and uv

Writing CRUD API for Postgres database. Repository for CRUD-operations, routers for them
and testing all the functionality with pytest (and asyncio).

## Usage

**Required:**

* configured .env file (for tests .env.test)
* Postgres database
* and use make commands

### Makefile commands

    make setup
Setting up virtual environment with uv

    make create-requirements
Compiling project dependencies to requirements.txt

    make start
Starting Uvicorn server with --reload and on port 8001

    make tests
Running tests from /tests folder

    make create-revision
Creating a database revision

    make migrate-head
Upgrading to head revision

    make lint
Linter project

    make lint-fix
Try to use ruff for fix some problems

#### DB cli commands

    make db-create
Creating database

    make db-drop
Drop database

    make db-tables
Creating tables in database

    make db-all
Inserting all jsons from /data folder

    make db-base
Inserting base jsons (configured in /src/core/cli/utils.py) from /data folder
