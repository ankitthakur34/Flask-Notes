def test_auth_headers(
    auth_headers
):

    assert "Authorization" in auth_headers

    assert auth_headers[
        "Authorization"
    ].startswith(
        "Bearer "
    )