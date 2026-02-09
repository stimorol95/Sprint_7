import pytest
import allure
import requests
from helpers.api_client import APIHelper
from helpers.data_generator import generate_courier_data
from data.urls import URLs


class TestLoginCourier:
    @allure.title("Курьер может авторизоваться")
    def test_login_courier_success(self):
        api = APIHelper()
        data = generate_courier_data()
        with allure.step("Создать курьера"):
            api.courier.create_courier(data)
        with allure.step("Авторизовать курьера"):
            login_result = api.courier.login_courier(data["login"], data["password"])
        with allure.step("Очистить тестовые данные"):
            api.courier.delete_courier_by_credentials(data["login"], data["password"])
        assert login_result["status_code"] == 200 and login_result["success"] is True
    
    @allure.title("Успешная авторизация возвращает id")
    def test_successful_login_returns_id(self):
        api = APIHelper()
        data = generate_courier_data()
        with allure.step("Создать курьера"):
            api.courier.create_courier(data)
        with allure.step("Авторизовать курьера"):
            login_result = api.courier.login_courier(data["login"], data["password"])
        with allure.step("Очистить тестовые данные"):
            api.courier.delete_courier_by_credentials(data["login"], data["password"])
        assert "id" in login_result["json_data"]
    
    @allure.title("Нельзя авторизоваться с неправильным паролем")
    def test_login_with_wrong_password_fails(self):
        api = APIHelper()
        data = generate_courier_data()
        with allure.step("Создать курьера"):
            api.courier.create_courier(data)
        with allure.step("Попытаться авторизоваться с неправильным паролем"):
            login_result = api.courier.login_courier(data["login"], "wrong_password")
        with allure.step("Очистить тестовые данные"):
            api.courier.delete_courier_by_credentials(data["login"], data["password"])
        assert login_result["status_code"] == 404
    
    @allure.title("Нельзя авторизоваться под несуществующим пользователем")
    def test_login_with_nonexistent_user_fails(self):
        api = APIHelper()
        with allure.step("Попытаться авторизоваться с несуществующим логином"):
            login_result = api.courier.login_courier("nonexistent_user", "any_password")
        assert login_result["status_code"] == 404
    
    @allure.title("Нельзя авторизоваться без логина")
    def test_login_without_login_fails(self):
        with allure.step("Отправить запрос авторизации без логина"):
            response = requests.post(URLs.LOGIN_COURIER, data={"password": "test"})
        assert response.status_code != 200
    
    @allure.title("Нельзя авторизоваться без пароля")
    def test_login_without_password_fails(self):
        with allure.step("Отправить запрос авторизации без пароля"):
            response = requests.post(URLs.LOGIN_COURIER, data={"login": "test"})
        assert response.status_code != 20