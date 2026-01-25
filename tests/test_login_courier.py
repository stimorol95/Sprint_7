import pytest
import requests
import allure


class TestLoginCourier:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    
    def create_courier(self):
        from conftest import generate_courier_data  
        data = generate_courier_data()
        response = requests.post(f'{self.BASE_URL}/api/v1/courier', data=data)
        return data, response
    
    def login_courier(self, login, password):
        payload = {"login": login, "password": password}
        return requests.post(f'{self.BASE_URL}/api/v1/courier/login', data=payload)
    
    def delete_courier(self, courier_id):
        return requests.delete(f'{self.BASE_URL}/api/v1/courier/{courier_id}')
    
    @allure.title("Курьер может авторизоваться")
    def test_login_courier_success(self):
        data, create_response = self.create_courier()
        login_response = self.login_courier(data["login"], data["password"])
        
        if login_response.status_code == 200:
            self.delete_courier(login_response.json()["id"])
        
        assert login_response.status_code == 200 and "id" in login_response.json()
    
    @allure.title("Нельзя авторизоваться с неправильным паролем")
    def test_login_with_wrong_password_fails(self):
        data, create_response = self.create_courier()
        login_response = self.login_courier(data["login"], "wrong_password")
        
        correct_login = self.login_courier(data["login"], data["password"])
        if correct_login.status_code == 200:
            self.delete_courier(correct_login.json()["id"])
        
        assert login_response.status_code == 404
    
    @allure.title("Нельзя авторизоваться под несуществующим пользователем")
    def test_login_with_nonexistent_user_fails(self):
        response = self.login_courier("nonexistent_user", "any_password")
        assert response.status_code == 404
    
    @allure.title("Нельзя авторизоваться без логина")
    def test_login_without_login_fails(self):
        response = requests.post(f'{self.BASE_URL}/api/v1/courier/login', data={"password": "test"})
        assert response.status_code != 200
    
    @allure.title("Нельзя авторизоваться без пароля")
    def test_login_without_password_fails(self):
        response = requests.post(f'{self.BASE_URL}/api/v1/courier/login', data={"login": "test"})
        assert response.status_code != 200