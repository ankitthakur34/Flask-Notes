from app.models import User


def test_get_user_success(
    client,
    test_user
):

    response = client.get(

        f"/users/{test_user.id}"

    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["data"]["id"] == test_user.id

    assert data["data"]["username"] == test_user.username

    assert data["data"]["email"] == test_user.email

def test_get_user_not_found(client):

    response = client.get(

        "/users/99999"

    )

    assert response.status_code == 404