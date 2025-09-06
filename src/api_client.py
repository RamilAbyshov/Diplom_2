import requests
import allure
from src.data import REGISTER_URL, LOGIN_URL, USER_URL, ORDERS_URL, INGREDIENTS_URL


class UserAPI:

    @staticmethod
    @allure.step("Регистрация пользователя")
    def register(email, password, name):
        payload = {"email": email, "password": password, "name": name}
        return requests.post(REGISTER_URL, json=payload)

    @staticmethod
    @allure.step("Логин пользователя")
    def login(email, password):
        payload = {"email": email, "password": password}
        return requests.post(LOGIN_URL, json=payload)

    @staticmethod
    @allure.step("Обновление данных пользователя")
    def update(access_token, data):
        headers = {"Authorization": access_token}
        return requests.patch(USER_URL, headers=headers, json=data)

    @staticmethod
    @allure.step("Удаление пользователя")
    def delete(access_token):
        headers = {"Authorization": access_token}
        return requests.delete(USER_URL, headers=headers)


class OrderAPI:

    @staticmethod
    @allure.step("Создание заказа")
    def create(access_token, ingredients):
        headers = {"Authorization": access_token} if access_token else {}
        payload = {"ingredients": ingredients}
        return requests.post(ORDERS_URL, headers=headers, json=payload)

    @staticmethod
    @allure.step("Получение заказов пользователя")
    def get_user_orders(access_token):
        headers = {"Authorization": access_token} if access_token else {}
        return requests.get(ORDERS_URL, headers=headers)

    @staticmethod
    @allure.step("Получение id ингредиентов")
    def get_ingredient_ids():
        response = requests.get(INGREDIENTS_URL)
        response.raise_for_status()
        return [item["_id"] for item in response.json()["data"]]