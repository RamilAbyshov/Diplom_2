import allure
import pytest
from src import helpers
from src.api_client import UserAPI
from src.data import ERROR_MESSAGES


@allure.feature("Регистрация пользователя")
class TestRegisterUser:

    @allure.title("Создание уникального пользователя")
    @allure.description("Проверяем, что можно зарегистрировать нового уникального пользователя.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_unique_user(self):
        user_data = helpers.random_user_data()
        response = UserAPI.register(
            user_data["email"],
            user_data["password"],
            user_data["name"]
        )

        # Проверяем успешную регистрацию
        assert response.status_code == 200
        assert response.json()["success"] is True

        # Удаляем созданного пользователя после теста
        access_token = response.json().get("accessToken")
        delete_response = UserAPI.delete(access_token)
        assert delete_response.status_code == 202

    @allure.title("Регистрация уже существующего пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_existing_user(self, create_user):
        response = UserAPI.register(create_user["email"], create_user["password"], create_user["name"])
        assert response.status_code == 403
        assert response.json()["message"] == ERROR_MESSAGES["user_exists"]

    @allure.title("Регистрация без обязательного поля")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "email, password, name, missing_field",
        [
            ("", "123456", "TestUser", "email"),
            ("no_name@test.com", "123456", "", "name"),
            ("no_pass@test.com", "", "TestUser", "password"),
        ]
    )
    def test_create_user_without_required_field(self, email, password, name, missing_field):
        response = UserAPI.register(email, password, name)
        assert response.status_code == 403
        assert ERROR_MESSAGES["required_fields"].split()[0] in response.json()["message"]