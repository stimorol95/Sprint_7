import pytest
from helpers.api_client import APIHelper
from helpers.data_generator import generate_courier_data


@pytest.fixture
def api_client():
    """Фикстура для создания API клиента"""
    return APIHelper()

@pytest.fixture
def create_courier():
    """Фикстура для создания и удаления курьера"""
    api = APIHelper()
    data = generate_courier_data()
    create_result = api.courier.create_courier(data)
    if create_result["status_code"] != 201:
        pytest.skip(f"Не удалось создать курьера: {create_result['status_code']}")
    yield data, api
    api.courier.delete_courier_by_credentials(data["login"], data["password"])