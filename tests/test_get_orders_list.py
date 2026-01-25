import pytest
import requests
import allure


class TestGetOrdersList:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    
    @allure.title("Получение списка заказов")
    def test_get_orders_list_returns_list(self):
        response = requests.get(f'{self.BASE_URL}/api/v1/orders')
        assert response.status_code == 200 and isinstance(response.json().get("orders", []), list)