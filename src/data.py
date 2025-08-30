# URL
BASE_URL = "https://stellarburgers.nomoreparties.site/api"

# Ручки

REGISTER_URL = f"{BASE_URL}/auth/register"
LOGIN_URL = f"{BASE_URL}/auth/login"
USER_URL = f"{BASE_URL}/auth/user"
ORDERS_URL = f"{BASE_URL}/orders"
INGREDIENTS_URL = f"{BASE_URL}/ingredients"

# Сообщения ошибок
ERROR_MESSAGES = {
    "unauthorized": "You should be authorised",
    "user_exists": "User already exists",
    "required_fields": "Email, password and name are required",
    "missing_ingredient": "Ingredient ids must be provided",
    "unexpected_status": "Status code does not match expected"
}