from app.models import User


def test_register_success(client):

    payload = {

        "username": "ankit",

        "email": "ankit@test.com",

        "password": "Password123"
    }

    response = client.post(

        "/register",

        json=payload
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["success"] is True

    assert data["message"] == "User registered successfully"

    user = User.query.filter_by(

        email="ankit@test.com"

    ).first()

    assert user is not None

    assert user.username == "ankit"

    assert user.is_verified is False

    assert user.password != "Password123"

    assert user.check_password(
        "Password123"
    )


def test_register_duplicate_email(client, test_user):

    payload = {

        "username": "newuser",

        "email": test_user.email,

        "password": "Password123"
    }

    response = client.post(

        "/register",

        json=payload
    )

    assert response.status_code == 409

    data = response.get_json()

    assert data["success"] is False

def test_register_duplicate_username(client, test_user):

    payload = {

        "username": test_user.username,

        "email": "new@test.com",

        "password": "Password123"
    }

    response = client.post(

        "/register",

        json=payload
    )

    assert response.status_code == 409


def test_register_invalid_email(client):

    payload = {

        "username": "ankit",

        "email": "abc",

        "password": "Password123"
    }

    response = client.post(

        "/register",

        json=payload
    )

    assert response.status_code == 400

def test_register_missing_password(client):

    payload = {

        "username": "ankit",

        "email": "ankit@test.com"
    }

    response = client.post(

        "/register",

        json=payload
    )

    assert response.status_code == 400

def test_register_empty_body(client):

    response = client.post(

        "/register",

        json={}
    )

    assert response.status_code == 400

def test_password_is_hashed(client):

    payload = {

        "username": "ankit",

        "email": "ankit@test.com",

        "password": "Password123"
    }

    client.post(

        "/register",

        json=payload
    )

    user = User.query.filter_by(

        email="ankit@test.com"

    ).first()

    assert user.check_password(
        "Password123"
    )