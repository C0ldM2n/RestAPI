# @pytest.fixture
# def test_files(tmp_path):
#     """Fixture for test JSON files in a temporary directory."""
#     brands_data = [{'id': 1, 'country_registration_id': None, 'name': 'TestBrand'}]
#     categories_data = [{'id': 1, 'name': 'TestCategory'}]
#
#     brands_path = tmp_path / 'brands.json'
#     categories_path = tmp_path / 'categories.json'
#
#     brands_path.write_text(json.dumps(brands_data))
#     categories_path.write_text(json.dumps(categories_data))
#
#     return [brands_path, categories_path]