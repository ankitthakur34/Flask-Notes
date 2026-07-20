from .base import BaseConfig


class TestingConfig(
    BaseConfig
):

    DEBUG = False

    TESTING = True
    LOG_LEVEL = "INFO"

    REQUIRE_EMAIL_VERIFICATION = False

    ENV_NAME = "testing"