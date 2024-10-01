import json
from pathlib import Path
from http.client import responses

import pytest

from httpx import AsyncClient
from sqlalchemy.orm import session
from sqlalchemy.ext.asyncio import AsyncSession

import models
from core.db.database import get_async_session
from core.cli import (bulk_insert_data_from_files,
                      bulk_insert_base_jsons, bulk_insert_all_jsons)


@pytest.mark.asyncio
async def test_bulk_insert_base(db_session):
    async with db_session:
        await bulk_insert_base_jsons()


# @pytest.mark.asyncio
# async def test_bulk_insert_all(db_session):
#     async with db_session:
#         await bulk_insert_all_jsons()




# @pytest.mark.asyncio
# async def test_bulk_create_brands(session: AsyncSession = Depends(get_async_session)):
#     """Test bulk creation of brands."""
#     file_path: list[Path] = [Path(__file__).parent.parent.parent / 'data' / 'brands.json']
#
#     response = runner.invoke(app, ["bulk_insert_from_files"], file_path)


# @pytest.mark.asyncio
# async def test_bulk_create_categories(session: AsyncSession = Depends(get_async_session)):
#     """Test bulk creation of brands."""
#     file_path: list[Path] = [Path(__file__).parent.parent.parent / 'data' / 'categories.json']
#
#     response = await bulk_insert_data_from_files(file_path, session)


# @pytest.mark.asyncio
# async def test_bulk_create_products(session: AsyncSession = Depends(get_async_session)):
#     """Test bulk creation of brands."""
#     file_path: list[Path] = [Path(__file__).parent.parent.parent / 'data' / 'products.json']
#
#     response = await bulk_insert_data_from_files(file_path, session)
