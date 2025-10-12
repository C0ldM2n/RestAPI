




# @pytest.mark.asyncio
# async def test_bulk_create_products(client: AsyncClient):
#     """Test bulk creation of products."""
#     file_path = Path(__file__).parent.parent / 'data' / 'products.json'
#
#     with open(file_path) as f:
#         products = json.load(f)
#
#     response = await client.post("/products/bulk-create-products", json=products)
#     assert response.status_code == status.HTTP_201_CREATED, (f"Unexpected status code: {response.status_code}. "
#                                                              f"Response text: {response.text}")
#
#     response_data = response.json()
#
#     assert len(response_data) == len(products)
#     for product, original_product in zip(response_data, products):
#         assert product['name'] == original_product['name']
#         assert product['price'] == original_product['price']
#         assert product['sku'] == original_product['sku']
