def test_login_success(
    client,
    test_user
):

    payload = {

        "email": test_user.email,

        "password": "Password123"
    }

    response = client.post(

        "/login",

        json=payload
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True

    assert "access_token" in data["data"]

    assert "refresh_token" in data["data"]

    assert isinstance(
        data["data"]["access_token"],
        str
    )

def test_login_wrong_password(
    client,
    test_user
):

    payload = {

        "email": test_user.email,

        "password": "WrongPassword"
    }

    response = client.post(

        "/login",

        json=payload
    )

    assert response.status_code == 401

def test_login_user_not_found(client):

    payload = {

        "email": "abc@test.com",

        "password": "Password123"
    }

    response = client.post(

        "/login",

        json=payload
    )

    assert response.status_code == 401

def test_login_missing_email(client):

    response = client.post(

        "/login",

        json={

            "password": "Password123"
        }
    )

    assert response.status_code == 400

def test_login_missing_password(client):

    response = client.post(

        "/login",

        json={

            "email": "abc@test.com"
        }
    )

    assert response.status_code == 400

def test_login_invalid_email(client):

    response = client.post(

        "/login",

        json={

            "email": "abc",

            "password": "Password123"
        }
    )

    assert response.status_code == 400