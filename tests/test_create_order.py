import pytest
import allure
from helpers.api_client import APIHelper
from helpers.data_generator import generate_order_data


class TestCreateOrder:
    @allure.title("Создание заказа с разными параметрами цветов")
    @pytest.mark.parametrize("color, test_name", [
        ("BLACK", "заказ с черным цветом"),
        ("GREY", "заказ с серым цветом"),
        (["BLACK", "GREY"], "заказ с двумя цветами"),
        (None, "заказ без указания цвета")
    ])
    def test_create_order_with_different_colors(self, color, test_name):
        api = APIHelper()
        with allure.step(f"Сгенерировать данные заказа ({test_name})"):
            data = generate_order_data(color)
        with allure.step("Создать заказ"):
            result = api.order.create_order(data)
        assert result["status_code"] == 201 and result["success"] is True

    @allure.title("Создание заказа возвращает track номер")
    @pytest.mark.parametrize("color", ["BLACK", "GREY", ["BLACK", "GREY"], None])
    def test_create_order_returns_track(self, color):
        api = APIHelper()
        with allure.step("Сгенерировать данные заказа"):
            data = generate_order_data(color)
        with allure.step("Создать заказ и проверить наличие track"):
            result = api.order.create_order(data)
        assert "track" in result["json_data"]