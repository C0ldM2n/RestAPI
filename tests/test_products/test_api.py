import json
from pathlib import Path

import pytest

from httpx import AsyncClient

from fastapi import status

from src.products.routers import router


# class TestProductsAPI:
#     """Test cases for the ingredients API."""
#
#     async def test_create_products(self, client):
#         response = await client.post(router.prefix, json={"name": "TestPhone", "price": "1000"})
#         print(response.json())
#         assert response.status_code == status.HTTP_201_CREATED
#         product_id = response.json().get("id")
#         assert product_id is not None
#
#         response = await client.get(f"/{router.prefix}/{product_id}")
#         assert response.status_code == status.HTTP_200_OK
#         assert response.json()[0]["id"] == product_id
#         assert response.json()[0]["name"] == "TestPhone"

#
# @pytest.mark.asyncio
# async def test_create_products(client: AsyncClient):
#     """Test the creation of a product."""
#     file_path = Path(__file__).parent / 'fake_data' / 'products.json'
#
#     with open(file_path) as f:
#         products_data = json.load(f)
#
#     response = await client.post('/products/', json=products_data)
#
#     assert response.status_code == status.HTTP_201_CREATED
#
#     # Check if the number of products created matches
#     assert len(response.json()) == len(products_data)


@pytest.mark.asyncio
async def test_bulk_create_products(client: AsyncClient):
    """Test bulk creation of products."""
    file_path = Path(__file__).parent / 'fake_data' / 'products.json'

    with open(file_path) as f:
        products = json.load(f)

    response = await client.post("/products/bulk_create_products", json=products)
    assert response.status_code == status.HTTP_201_CREATED

    # assert response.status_code == status.HTTP_201_CREATED, (f"Unexpected status code: {response.status_code}. "
    #                                                          f"Response text: {response.text}")

    # Check if products are created
    response_data = response.json()

    assert len(response_data) == len(products)
    for product, original_product in zip(response_data, products):
        assert product['name'] == original_product['name']
        assert product['price'] == original_product['price']
        assert product['sku'] == original_product['sku']
