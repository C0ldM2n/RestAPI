import asyncio
from pathlib import Path

import typer

from core.db.database import get_async_session
from .utils import bulk_insert_data_from_files, bulk_insert_base_jsons, bulk_insert_all_jsons

app = typer.Typer()


# @app.command()
# def bulk_insert(
#     files: list[Path] = typer.Argument(..., help="Paths to JSON files for bulk insertion.")):
#     """Bulk insert data into tables from specified JSON files."""
#     try:
#         bulk_insert_data_from_files(files)
#         typer.echo("Data inserted successfully.")
#     except Exception as e:
#         typer.echo(f"Error occurred: {e}")


@app.command("bulk_insert_base_jsons")
def bulk_insert_base():
    """Bulk insert base data (brands, categories)."""
    asyncio.run(bulk_insert_base_jsons())


@app.command("bulk_insert_all_jsons")
def bulk_insert_all():
    """Bulk insert all available JSON files."""
    asyncio.run(bulk_insert_all_jsons())


# @app.command()
# def bulk_insert_all():
#     """Bulk insert all available JSON files."""
#     with get_async_session() as session:
#         try:
#             bulk_insert_all_jsons(session)
#             typer.echo("All data inserted successfully.")
#         except Exception as e:
#             typer.echo(f"Error occurred: {e}")

if __name__ == "__main__":
    app()
