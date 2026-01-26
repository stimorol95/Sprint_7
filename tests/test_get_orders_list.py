import pytest
import allure
from helpers.api_client import APIHelper


class TestGetOrdersList:
    
    @allure.title("Можно получить список заказов")
    def test_can_get_orders_list(self):
        api = APIHelper()
        with allure.step("Запросить список заказов"):
            result = api.order.get_orders_list()
        assert result["status_code"] == 200 and result["success"] is True
    
    @allure.title("Список заказов возвращает orders")
    def test_orders_list_contains_orders(self):
        api = APIHelper()
        with allure.step("Запросить список заказов"):
            result = api.order.get_orders_list()
        assert "orders" in result["json_data"]