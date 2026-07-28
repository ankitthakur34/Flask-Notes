def test_profile_upload_url(

    client,

    auth_headers,

    mock_s3
):

    response = client.post(

        "/profile/upload-url",

        headers=auth_headers,

        json={

            "filename": "photo.jpg",

            "content_type": "image/jpeg"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert (

        data["data"]["upload_url"]

        ==

        "https://fake-url.com"
    )

    mock_s3.get_upload_url.assert_called_once()


# def test_profile_upload_url_failure(

#     client,

#     auth_headers,

#     mock_s3_failure
# ):

#     response = client.post(

#         "/profile/upload-url",

#         headers=auth_headers,

#         json={

#             "filename": "photo.jpg",

#             "content_type": "image/jpeg"
#         }
#     )

#     assert response.status_code == 200

#     data = response.get_json()

#     assert (

#         data["data"]["upload_url"]

#         ==

#         "https://fake-url.com"
#     )

#     mock_s3_failure.get_upload_url.assert_called_once()    