import requests
import allure
import json
from data.urls import URLs


class BaseAPI:
    def _parse_response(self, response: requests.Response) -> dict:
        """Парсит ответ и возвращает структурированные данные"""
        result = {
            "success": 200 <= response.status_code < 300,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "url": response.url,
            "text": response.text,
            "json_data": None,
            "error": None
        }
        
        if response.text and response.text.strip():
            try:
                result["json_data"] = response.json()
            except json.JSONDecodeError:
                result["error"] = "Response is not valid JSON"
        return result


class CourierAPI(BaseAPI):
    @allure.step("Создать курьера")
    def create_courier(self, data: dict) -> dict:
        response = requests.post(URLs.CREATE_COURIER, data=data)
        return self._parse_response(response)
    
    @allure.step("Авторизовать курьера")
    def login_courier(self, login: str, password: str) -> dict:
        payload = {"login": login, "password": password}
        response = requests.post(URLs.LOGIN_COURIER, data=payload)
        return self._parse_response(response)
    
    @allure.step("Удалить курьера")
    def delete_courier(self, courier_id: int) -> dict:
        response = requests.delete(f"{URLs.DELETE_COURIER}/{courier_id}")
        return self._parse_response(response)
    
    @allure.step("Удалить курьера по логину и паролю")
    def delete_courier_by_credentials(self, login: str, password: str) -> dict:
        login_result = self.login_courier(login, password)
        if login_result["success"] and "id" in login_result.get("json_data", {}):
            return self.delete_courier(login_result["json_data"]["id"])
        return self._parse_response(requests.Response())


class OrderAPI(BaseAPI):
    @allure.step("Создать заказ")
    def create_order(self, data: dict) -> dict:
        response = requests.post(URLs.CREATE_ORDER, json=data)
        return self._parse_response(response)
    
    @allure.step("Получить список заказов")
    def get_orders_list(self) -> dict:
        response = requests.get(URLs.GET_ORDERS_LIST)
        return self._parse_response(response)

class APIHelper:
    def __init__(self):
        self.courier = CourierAPI()
        self.order = OrderAPI()