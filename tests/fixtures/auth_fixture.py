import pytest

from flask_jwt_extended import (
    create_access_token
)


@pytest.fixture
def auth_headers(
    app,
    test_user
):

    with app.app_context():

        token = create_access_token(
            identity=str(test_user.id)
        )

    return {

        "Authorization":
        f"Bearer {token}"
    }