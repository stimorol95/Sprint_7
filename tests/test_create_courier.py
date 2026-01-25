import pytest
import requests
import allure


class TestCreateCourier:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    
    def register_courier(self, data):
        response = requests.post(f'{self.BASE_URL}/api/v1/courier', data=data)
        return response
    
    def login_courier(self, login, password):
        payload = {"login": login, "password": password}
        return requests.post(f'{self.BASE_URL}/api/v1/courier/login', data=payload)
    
    def delete_courier(self, courier_id):
        return requests.delete(f'{self.BASE_URL}/api/v1/courier/{courier_id}')
    
    def cleanup_courier(self, login, password):
        login_resp = self.login_courier(login, password)
        if login_resp.status_code == 200:
            self.delete_courier(login_resp.json()["id"])
    
    @allure.title("Курьера можно создать")
    def test_create_courier_success(self):
        from conftest import generate_courier_data
        data = generate_courier_data()
        response = self.register_courier(data)
        self.cleanup_courier(data["login"], data["password"])
        assert response.status_code == 201 and response.json() == {"ok": True}
    
    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self):
        from conftest import generate_courier_data
        data = generate_courier_data()
        self.register_courier(data)
        duplicate_response = self.register_courier(data)
        self.cleanup_courier(data["login"], data["password"])
        assert duplicate_response.status_code == 409
    
    @allure.title("Нельзя создать курьера без логина")
    def test_create_courier_without_login_fails(self):
        from conftest import generate_courier_data
        data = generate_courier_data()
        del data["login"]
        response = self.register_courier(data)
        assert response.status_code == 400
    
    @allure.title("Нельзя создать курьера без пароля")
    def test_create_courier_without_password_fails(self):
        from conftest import generate_courier_data
        data = generate_courier_data()
        del data["password"]
        response = self.register_courier(data)
        assert response.status_code == 400
    
    @allure.title("Тест на создание курьера без firstName")
    def test_create_courier_without_firstname(self):
        from conftest import generate_courier_data
        data = generate_courier_data()
        del data["firstName"]
        response = self.register_courier(data)
        if response.status_code == 201:
            self.cleanup_courier(data["login"], data["password"])
        assert response.status_code != 500