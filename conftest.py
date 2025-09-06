import pytest
import allure
from src import helpers
from src.api_client import UserAPI


@pytest.fixture
def create_user():
    email = helpers.random_email()
    password = helpers.random_password()
    name = helpers.random_name()

    with allure.step("Регистрация тестового пользователя"):
        response = UserAPI.register(email, password, name)
        access_token = response.json().get("accessToken")

    yield {"email": email, "password": password, "name": name, "accessToken": access_token}

    with allure.step("Удаление тестового пользователя после теста"):
        if access_token:
            UserAPI.delete(access_token)