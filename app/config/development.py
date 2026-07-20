from .base import BaseConfig


class DevelopmentConfig(
    BaseConfig
):

    DEBUG = True

    ENV_NAME = "development"

    REQUIRE_EMAIL_VERIFICATION = False