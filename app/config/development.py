from .base import BaseConfig


class DevelopmentConfig(
    BaseConfig
):

    DEBUG = True
    LOG_LEVEL = "DEBUG"

    ENV_NAME = "development"

    REQUIRE_EMAIL_VERIFICATION = False