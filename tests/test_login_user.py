import allure
from src import helpers

@allure.feature("Авторизация пользователя")
class TestLoginUser:

    @allure.title("Логин под существующим пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_existing_user(self, create_user):
        response = helpers.login_user(create_user["email"], create_user["password"])
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Логин с неверным логином и паролем")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_with_invalid_data(self):
        response = helpers.login_user("wrong@test.com", "wrongpass")
        assert response.status_code == 401
        assert "email or password" in response.json()["message"]
