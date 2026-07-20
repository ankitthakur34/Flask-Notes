from .base import BaseConfig


class ProductionConfig(
    BaseConfig
):

    DEBUG = False

    ENV_NAME = "production"

    REQUIRE_EMAIL_VERIFICATION = True