from unittest.mock import ANY
def test_register_sends_email(

    client,

    mock_send_email
):

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

    mock_send_email.assert_called_once_with(

    "ankit@test.com",

    "Verify Your Email",

    ANY
)


def test_email_failure(

    client,

    mock_send_email_failure
):

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

    mock_send_email_failure.assert_called_once()