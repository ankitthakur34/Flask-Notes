
import pytest
from tests.fixtures.user_fixture import *
from tests.fixtures.auth_fixture import *
from tests.fixtures.mock_email import *
from tests.fixtures.mock_s3 import *
from app import create_app
from app.extensions import db


@pytest.fixture
def app():

    app = create_app()

    with app.app_context():

        db.create_all()

        yield app

        db.session.remove()

        db.drop_all()


@pytest.fixture
def client(app):

    return app.test_client()