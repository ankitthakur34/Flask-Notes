from .base import BaseConfig


class ProductionConfig(
    BaseConfig
):

    DEBUG = False
    LOG_LEVEL = "WARNING"

    ENV_NAME = "production"

    REQUIRE_EMAIL_VERIFICATION = True