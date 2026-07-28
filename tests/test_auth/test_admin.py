def test_get_users_admin(

    client,

    admin_headers
):

    response = client.get(

        "/users",

        headers=admin_headers
    )

    assert response.status_code == 200

def test_get_users_normal_user(

    client,

    auth_headers
):

    response = client.get(

        "/users",

        headers=auth_headers
    )

    assert response.status_code == 403
def test_get_users_without_token(

    client
):

    response = client.get(

        "/users"
    )

    assert response.status_code == 401        