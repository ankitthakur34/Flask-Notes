import pytest

from unittest.mock import patch


@pytest.fixture
def mock_send_email():

    with patch(

        "app.services.auth_service.send_email_task.delay"

    ) as mock:

        yield mock

@pytest.fixture
def mock_send_email_failure():

    with patch(

        "app.services.auth_service.send_email_task.delay"

    ) as mock:

        mock.side_effect = Exception(

            "Celery Down"
        )

        yield mock