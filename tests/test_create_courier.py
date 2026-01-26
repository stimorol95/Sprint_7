import pytest
import allure
from helpers.api_client import APIHelper
from helpers.data_generator import generate_courier_data


class TestCreateCourier:
    @allure.title("Курьера можно создать")
    def test_create_courier_success(self):
        api = APIHelper()
        data = generate_courier_data()
        with allure.step("Создать курьера с валидными данными"):
            result = api.courier.create_courier(data)
        with allure.step("Очистить тестовые данные"):
            api.courier.delete_courier_by_credentials(data["login"], data["password"])
        assert result["status_code"] == 201 and result["success"] is True
    
    @allure.title("Успешное создание курьера возвращает ok: true")
    def test_create_courier_returns_ok_true(self):
        api = APIHelper()
        data = generate_courier_data()
        with allure.step("Создать курьера"):
            result = api.courier.create_courier(data)
        with allure.step("Очистить тестовые данные"):
            api.courier.delete_courier_by_credentials(data["login"], data["password"])
        assert result["json_data"] == {"ok": True}
    
    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self):
        api = APIHelper()
        data = generate_courier_data()
        with allure.step("Создать первого курьера"):
            api.courier.create_courier(data)
        with allure.step("Попытаться создать второго курьера с тем же логином"):
            duplicate_result = api.courier.create_courier(data)
        with allure.step("Очистить тестовые данные"):
            api.courier.delete_courier_by_credentials(data["login"], data["password"])
        assert duplicate_result["status_code"] == 409
    
    @allure.title("Нельзя создать курьера без логина")
    def test_create_courier_without_login_fails(self):
        api = APIHelper()
        data = generate_courier_data()
        del data["login"]
        with allure.step("Создать курьера без логина"):
            result = api.courier.create_courier(data)
        assert result["status_code"] != 201 and result["success"] is False
    
    @allure.title("Нельзя создать курьера без пароля")
    def test_create_courier_without_password_fails(self):
        api = APIHelper()
        data = generate_courier_data()
        del data["password"]
        with allure.step("Создать курьера без пароля"):
            result = api.courier.create_courier(data)
        assert result["status_code"] != 201 and result["success"] is False