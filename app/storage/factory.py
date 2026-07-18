from flask import current_app

from app.storage.local_storage import (
    LocalStorageService
)

from app.storage.s3_storage import (
    S3StorageService
)


def get_storage():

    provider = current_app.config[
        "UPLOAD_PROVIDER"
    ]

    if provider == "LOCAL":

        return LocalStorageService()

    if provider == "S3":

        return S3StorageService()

    raise ValueError(
        f"Unsupported storage provider: {provider}"
    )


def get_attachment_folder():

    if current_app.config[
        "UPLOAD_PROVIDER"
    ] == "S3":

        return current_app.config[
            "ATTACHMENT_S3_FOLDER"
        ]

    return current_app.config[
        "ATTACHMENT_UPLOAD_FOLDER"
    ]


def get_profile_folder():

    if current_app.config[
        "UPLOAD_PROVIDER"
    ] == "S3":

        return current_app.config[
            "PROFILE_S3_FOLDER"
        ]

    return current_app.config[
        "PROFILE_UPLOAD_FOLDER"
    ]