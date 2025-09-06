import allure
from src import helpers
from src.api_client import OrderAPI, UserAPI
from src.data import ERROR_MESSAGES

@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_auth_and_ingredients(self, create_user):
        ingredient_ids = OrderAPI.get_ingredient_ids()
        response = OrderAPI.create(create_user["accessToken"], [ingredient_ids[0], ingredient_ids[1], ingredient_ids[2]])
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_auth(self):
        ingredient_ids = OrderAPI.get_ingredient_ids()
        response = OrderAPI.create(None, [ingredient_ids[1], ingredient_ids[2], ingredient_ids[3]])
        assert response.status_code == 401
        assert ERROR_MESSAGES["unauthorized"] in response.json()["message"]

    @allure.title("Создание заказа без ингредиентов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_ingredients(self, create_user):
        response = OrderAPI.create(create_user["accessToken"], [])
        assert response.status_code == 400
        assert ERROR_MESSAGES["missing_ingredient"] in response.json()["message"]

    @allure.title("Создание заказа с неверным хэшем ингредиентов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_invalid_hash(self, create_user):
        response = OrderAPI.create(create_user["accessToken"], ["invalid_hash"])
        assert response.status_code == 500