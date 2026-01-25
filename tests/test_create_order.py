import pytest
import requests
import allure


class TestCreateOrder:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    
    @allure.title("Создание заказа с разными вариантами цветов")
    @pytest.mark.parametrize("color_param, description", [
        ("BLACK", "черный цвет"),
        ("GREY", "серый цвет"),
        (["BLACK", "GREY"], "оба цвета"),
        (None, "без указания цвета")
    ])
    def test_create_order_with_different_colors(self, color_param, description):
        from conftest import generate_order_data
        data = generate_order_data(color_param)
        response = requests.post(f'{self.BASE_URL}/api/v1/orders', json=data)
        assert response.status_code == 201 and "track" in response.json()