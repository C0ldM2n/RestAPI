from fastapi import status
from src.products.routers import router


class TestProductsAPI:
    """Test cases for the ingredients API."""

    async def test_create_products(self, client):
        response = await client.post(router.prefix, json={"name": "TestPhone", "price": "1000"})
        print(response.json())
        assert response.status_code == status.HTTP_201_CREATED
        product_id = response.json().get("id")
        assert product_id is not None

        response = await client.get(f"/{router.prefix}/{product_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]["id"] == product_id
        assert response.json()[0]["name"] == "TestPhone"
