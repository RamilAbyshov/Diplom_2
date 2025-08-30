import requests
from faker import Faker
from src.data import REGISTER_URL, LOGIN_URL, USER_URL, ORDERS_URL, INGREDIENTS_URL

fake = Faker('ru_RU')

# ---- Генерация тестовых данных пользователя ----

# Генерация случайных данных с помощью Faker
def random_email():
    return fake.email()

def random_password(length=10):
    return fake.password(length=length, special_chars=True, digits=True, upper_case=True, lower_case=True)

def random_name():
    return fake.first_name()

# Генерация полного набора данных пользователя
def random_user_data():
    return {
        "email": random_email(),
        "password": random_password(),
        "name": random_name()
    }

# ---- Пользователь ----

# Регистрация пользователя
def register_user(email, password, name):
    payload = {"email": email, "password": password, "name": name}
    return requests.post(REGISTER_URL, json=payload)

# Логин пользователя
def login_user(email, password):
    payload = {"email": email, "password": password}
    return requests.post(LOGIN_URL, json=payload)

# Обновление пользователя
def update_user(access_token, data):
    headers = {"Authorization": access_token}
    return requests.patch(USER_URL, headers=headers, json=data)

# Удаление пользователя
def delete_user(access_token):
    headers = {"Authorization": access_token}
    return requests.delete(USER_URL, headers=headers)

# Создание пользователя с заказами
def create_user_with_orders(num_orders=1, ingredients_count=2):
    user_data = random_user_data()
    reg_response = register_user(user_data["email"], user_data["password"], user_data["name"])
    reg_response.raise_for_status()
    access_token = reg_response.json()["accessToken"]

    ingredient_ids = get_ingredient_ids()
    created_orders = []

    for i in range(num_orders):
        order = ingredient_ids[i:i+ingredients_count]
        create_order(access_token, order)
        created_orders.extend(order)

    return {
        "accessToken": access_token,
        "ingredients": created_orders
    }

# ---- Заказы ----

# Создание заказа
def create_order(access_token, ingredients):
    headers = {"Authorization": access_token} if access_token else {}
    payload = {"ingredients": ingredients}
    return requests.post(ORDERS_URL, headers=headers, json=payload)

# Получение заказов пользователя
def get_user_orders(access_token):
    headers = {"Authorization": access_token} if access_token else {}
    return requests.get(ORDERS_URL, headers=headers)

# Получение id ингредиентов
def get_ingredient_ids():
    response = requests.get(INGREDIENTS_URL)
    response.raise_for_status()
    return [item["_id"] for item in response.json()["data"]]

# Возвращает список всех ингредиентов из ответа API /orders
def extract_ingredients_from_orders(orders_response_json):
    return [ing for order in orders_response_json["orders"] for ing in order["ingredients"]]