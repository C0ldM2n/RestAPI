import json
from typing import Any
from pathlib import Path

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


# Priority mapping for tables
TABLE_PRIORITY = {
    "brands": 1,
    "categories": 2,
    "products": 3
}

# Mapping between filenames and table names
FILE_TABLE_MAPPING = {
    "brands.json": "brands",
    "categories.json": "categories",
    "products.json": "products"
}


async def load_json_file(file_path: Path) -> list[dict[str, Any]]:
    """Load JSON data from a file."""
    with open(file_path, 'r') as f:
        data = f.read()
        # print(f"Loaded data from {file_path}: {data}")  # Debug statement
        return json.loads(data)


async def bulk_insert_data(table_name: str, data: list[dict[str, Any]], session: AsyncSession):
    """Insert data into the specified table."""
    if not data:
        print(f"No data to insert for table {table_name}.")  # Debug statement
        return

    # Dynamically get the table model based on the table_name
    table_model = get_table_model(table_name)

    # Perform bulk insert using SQLAlchemy's insert statement
    stmt = insert(table_model).values(data)
    await session.execute(stmt)


async def bulk_insert_data_from_files(files: list[Path], session: AsyncSession):
    """Insert data into tables from multiple JSON files, sorted by priority."""
    file_data = []

    # Read and associate each file with its table
    for file_path in files:
        file_name = file_path.name
        table_name = FILE_TABLE_MAPPING.get(file_name)
        if not table_name:
            raise ValueError(f"Unknown table for file {file_name}.")

        data = await load_json_file(file_path)
        file_data.append((table_name, data))

    # Sort files by their priority
    file_data.sort(key=lambda x: TABLE_PRIORITY[x[0]])

    # Insert data in the sorted order
    for table_name, data in file_data:
        await bulk_insert_data(table_name, data, session)


def get_table_model(table_name: str):
    """Return the SQLAlchemy model class for the given table name."""
    from models import Brand, Category, Product

    if table_name == "brands":
        return Brand
    elif table_name == "categories":
        return Category
    elif table_name == "products":
        return Product
    else:
        raise ValueError(f"Unknown table name: {table_name}")
