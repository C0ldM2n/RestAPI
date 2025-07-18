import asyncio
from pathlib import Path

import typer

from core.cli.utils import (
    bulk_insert_data_from_files,
    bulk_insert_base_jsons,
    bulk_insert_all_jsons,
    create_database,
    drop_database,
    create_tables,
)

app = typer.Typer()


@app.command("bulk_insert_data_from_files")
def bulk_insert(
    files: list[Path] = typer.Argument(
        ..., help="Paths to JSON files for bulk insertion."
    )
):
    """Bulk insert data into tables from specified JSON files."""
    try:
        bulk_insert_data_from_files(files)
        typer.echo("Data inserted successfully.")
    except Exception as e:
        typer.echo(f"Error occurred: {e}")


@app.command("bulk_insert_base_jsons")
def bulk_insert_base():
    """Bulk insert base data (brands, categories)."""
    asyncio.run(bulk_insert_base_jsons())
    typer.echo("Inserted base jsons in database")


@app.command("bulk_insert_all_jsons")
def bulk_insert_all():
    """Bulk insert all available JSON files."""
    asyncio.run(bulk_insert_all_jsons())
    typer.echo("Inserted all jsons in database")


@app.command("create_database")
def create_db():
    """Create new database"""
    asyncio.run(create_database())
    typer.echo("Database created")


@app.command("drop_database")
def drop_db():
    """Delete database"""
    asyncio.run(drop_database())
    typer.echo("Database droped")


@app.command("create_tables")
def init_tables():
    """Creating tables"""
    asyncio.run(create_tables())
    typer.echo("Tables droped and created")


if __name__ == "__main__":
    app()
