from pathlib import Path

import typer

from core.db.database import get_async_session
from . import bulk_insert_data_from_files


app = typer.Typer()

@app.command()
async def bulk_insert(
    files: list[Path] = typer.Argument(..., help="Paths to JSON files for bulk insertion.")):
    """
    Bulk insert data into tables from specified JSON files.
    The order of insertion is determined by table dependencies.
    """
    async with get_async_session() as session:
        try:
            await bulk_insert_data_from_files(files, session)
            typer.echo("Data inserted successfully.")
        except Exception as e:
            typer.echo(f"Error occurred: {e}")

if __name__ == "__main__":
    app()
