import allure
from src import helpers
from src.api_client import OrderAPI
from src.data import ERROR_MESSAGES

@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_orders_authorized(self):
        user_with_orders = helpers.create_user_with_orders(num_orders=3, ingredients_count=2)
        response = OrderAPI.get_user_orders(user_with_orders["accessToken"])
        assert response.status_code == 200
        data = response.json()

        returned_ingredients = helpers.extract_ingredients_from_orders(data)

        assert (
                data["success"]
                and len(data["orders"]) == 3
                and all(ing in returned_ingredients for ing in user_with_orders["ingredients"])
        )

    @allure.title("Получение заказов без авторизации")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_orders_unauthorized(self):
        response = OrderAPI.get_user_orders(None)
        assert response.status_code == 401
        assert ERROR_MESSAGES["unauthorized"] in response.json()["message"]