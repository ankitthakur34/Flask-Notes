import pytest

from unittest.mock import patch


@pytest.fixture
def mock_s3():

    with patch(

        "app.services.profile_image_service.get_storage"

    ) as mock_storage:

        storage = mock_storage.return_value

        storage.get_upload_url.return_value = {

            "upload_url": "https://fake-url.com",

            "filename": "abc.jpg",

            "key": "profile/abc.jpg"
        }

        yield storage

@pytest.fixture
def mock_s3_failure():

    with patch(

        "app.services.profile_image_service.get_storage"

    ) as mock_storage:

        storage = mock_storage.return_value

        storage.get_upload_url.side_effect = Exception(

            "AWS Down"
        )

        yield storage