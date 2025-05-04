# REST API | Python 3.12, FastAPI, SQLAlchemy, Pydantic and uv
Writing CRUD API for Postgres database. Repository for CRUD-operations, routers for them 
and testing all the functionality with pytest (and asyncio).

## Usage
**Required:**
* configured .env file (for tests .env.test)
* Postgres database
* and use make commands

### Makefile commands:
    make start
Starting Uvicorn server with --reload and on port 8001

    make setup
Setting up virtual environment with uv

    make tests
Running tests from /tests folder

    make makemigration
Creating a database revision

    make migrate
Upgrading to head revision

    make lint
Linter project

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
