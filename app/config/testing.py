from .base import BaseConfig


class TestingConfig(
    BaseConfig
):

    DEBUG = True

    TESTING = True
    LOG_LEVEL = "INFO"

    REQUIRE_EMAIL_VERIFICATION = False

    ENV_NAME = "testing"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    UPLOAD_PROVIDER = "LOCAL"

    MAIL_SUPPRESS_SEND = True