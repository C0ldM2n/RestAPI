# REST API | Python 3.12, FastAPI, SQLAlchemy, Pydantic and Poetry
Writing CRUD API for Postgres database. Repository for CRUD-operations, routers for them 
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

[//]: # (##### CLI commands for Windows &#40;using python from website&#41;)

[//]: # ()
[//]: # (    make win-cli-createdb)

[//]: # (Creating database)

[//]: # ()
[//]: # (    make win-cli-dropdb)

[//]: # (Drop database)

[//]: # ()
[//]: # (    make win-cli-tables)

[//]: # (Creating tables in database)

[//]: # ()
[//]: # (    make win-cli-all)

[//]: # (Inserting all jsons from /data folder)

[//]: # ()
[//]: # (    make win-cli-base)

[//]: # (Inserting base jsons &#40;configured in /src/core/cli/utils.py&#41; from /data folder)
