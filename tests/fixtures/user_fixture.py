import pytest

from app.extensions import db
from app.models import User


@pytest.fixture
def test_user(app):

    user = User(
        username="ankit",
        email="ankit@test.com"
    )

    user.set_password(
        "Password123"
    )

    db.session.add(user)
    db.session.commit()

    return user