import pytest
from src import helpers


@pytest.fixture
def create_user():
    email = helpers.random_email()
    password = helpers.random_password()
    name = helpers.random_name()

    response = helpers.register_user(email, password, name)
    access_token = response.json().get("accessToken")

    yield {"email": email, "password": password, "name": name, "accessToken": access_token}
    if access_token:
        helpers.delete_user(access_token)


