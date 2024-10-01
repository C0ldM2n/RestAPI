import json
from typing import Any
from pathlib import Path

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import session_maker
from config import settings

TABLE_PRIORITY = {
    "brands": 1,
    "categories": 2,
    "products": 3
}

FILE_TABLE_MAPPING = {
    "brands.json": "brands",
    "categories.json": "categories",
    "products.json": "products"
}


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


async def load_json_file(file_path: Path) -> list[dict[str, Any]]:
    """Load JSON data from a file."""
    with open(file_path, 'r') as f:
        data = f.read()
        return json.loads(data)


async def bulk_insert_data(table_name: str, data: list[dict[str, Any]], session: AsyncSession):
    """Insert data into the specified table."""
    if not data:
        print(f"No data to insert for table {table_name}.")
        return

    table_model = get_table_model(table_name)

    stmt = insert(table_model).values(data)
    await session.execute(stmt)
    await session.commit()


async def bulk_insert_data_from_files(files: list[Path], session: AsyncSession):
    """Insert data into tables from multiple JSON files, sorted by priority."""
    file_data = []

    for file_path in files:
        file_name = file_path.name
        table_name = FILE_TABLE_MAPPING.get(file_name)
        if not table_name:
            raise ValueError(f"Unknown table for file {file_name}.")

        data = await load_json_file(file_path)
        file_data.append((table_name, data))

    file_data.sort(key=lambda x: TABLE_PRIORITY[x[0]])

    for table_name, data in file_data:
        await bulk_insert_data(table_name, data, session)


async def bulk_insert_base_jsons():
    """Bulk insert base data like brands and categories from the base JSON files."""
    async with session_maker() as session:
        base_jsons = ['brands.json', 'categories.json']
        base_files = [Path("/".join([settings.BASE_DIR, 'data', json_file])) for json_file in base_jsons]
        await bulk_insert_data_from_files(base_files, session)


async def bulk_insert_all_jsons():
    """Bulk insert all available JSON files from the data folder."""
    async with session_maker() as session:
        data_folder = Path("/".join([settings.BASE_DIR, "data"]))
        json_files = list(data_folder.glob('*.json'))
        await bulk_insert_data_from_files(json_files, session)
