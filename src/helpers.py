from faker import Faker
import allure
from src.api_client import UserAPI, OrderAPI

fake = Faker('ru_RU')

# ---- Генерация тестовых данных пользователя ----

@allure.step("Генерация случайного email")
def random_email():
    return fake.email()

@allure.step("Генерация случайного пароля")
def random_password(length=10):
    return fake.password(length=length, special_chars=True, digits=True, upper_case=True, lower_case=True)

@allure.step("Генерация случайного имени")
def random_name():
    return fake.first_name()

@allure.step("Генерация полного набора данных пользователя")
def random_user_data():
    return {
        "email": random_email(),
        "password": random_password(),
        "name": random_name()
    }

# ---- Вспомогательные функции для тестов ----

@allure.step("Создание пользователя с заказами")
def create_user_with_orders(num_orders=1, ingredients_count=2):
    user_data = random_user_data()
    reg_response = UserAPI.register(user_data["email"], user_data["password"], user_data["name"])
    reg_response.raise_for_status()
    access_token = reg_response.json()["accessToken"]

    ingredient_ids = OrderAPI.get_ingredient_ids()
    created_orders = []

    for i in range(num_orders):
        order = ingredient_ids[i:i+ingredients_count]
        OrderAPI.create(access_token, order)
        created_orders.extend(order)

    return {
        "accessToken": access_token,
        "ingredients": created_orders
    }

@allure.step("Извлечение ингредиентов из ответа заказов")
def extract_ingredients_from_orders(orders_response_json):
    return [ing for order in orders_response_json["orders"] for ing in order["ingredients"]]