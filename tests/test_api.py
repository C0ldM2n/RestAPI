from fastapi import status


class TestProductsAPI:
    """Test cases for the ingredients API."""

    async def test_create_products(self, client):
        res = await client.get("/products/1")
        print(res)
        response = await client.post("/products", json={"name": "TestPhone", "price": "1000"})
        assert response.status_code == status.HTTP_201_CREATED
        product_id = response.json().get("id")
        assert product_id is not None

        response = await client.get(f"/products/{product_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]["id"] == product_id
        assert response.json()[0]["name"] == "TestPhone"
