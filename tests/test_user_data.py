import pytest
import allure
from src import helpers
from src.api_client import UserAPI
from src.data import ERROR_MESSAGES


@allure.feature("Изменение данных пользователя")
class TestUserData:

    @allure.title("Изменение имени и email авторизованного пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("field", ["name", "email"])
    def test_change_user_data_authorized_visible_fields(self, create_user, field):
        new_data = helpers.random_user_data()
        response = UserAPI.update(create_user["accessToken"], {field: new_data[field]})
        assert response.status_code == 200
        assert response.json()["user"][field] == new_data[field]

    @allure.title("Изменение пароля авторизованного пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_change_user_data_authorized_password(self, create_user):
        new_data = helpers.random_user_data()
        response = UserAPI.update(create_user["accessToken"], {"password": new_data["password"]})
        assert response.status_code == 200

    @allure.title("Изменение данных без авторизации")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("field", ["name", "email", "password"])
    def test_change_user_data_unauthorized(self, field):
        new_data = helpers.random_user_data()
        response = UserAPI.update(None, {field: new_data[field]})
        assert response.status_code == 401
        assert ERROR_MESSAGES["unauthorized"] in response.json()["message"]