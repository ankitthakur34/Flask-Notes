from flask import current_app

from app.storage.local_storage import LocalStorageService


def get_storage():

    provider = current_app.config[
        "UPLOAD_PROVIDER"
    ]

    if provider == "LOCAL":

        return LocalStorageService()

    raise ValueError(
        f"Unsupported storage provider: {provider}"
    )