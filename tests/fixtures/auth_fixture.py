import pytest

from flask_jwt_extended import (
    create_access_token
)

from app.models import User
from app.extensions import db



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

@pytest.fixture
def admin_user():

    user = User(

        username="admin",

        email="admin@test.com",

        role="ADMIN",

        is_verified=True
    )

    user.set_password("Password123")

    db.session.add(user)

    db.session.commit()

    return user


@pytest.fixture
def admin_headers(admin_user):

    token = create_access_token(

        identity=str(admin_user.id),

        additional_claims={

            "role": "ADMIN"
        }
    )

    return {

        "Authorization":

        f"Bearer {token}"
    }