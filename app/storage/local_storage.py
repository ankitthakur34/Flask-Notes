from flask import (
    current_app,
    send_from_directory
)

from app.storage.storage_service import StorageService

from app.utils.file_util import (
    save_file,
    delete_file
)

import os


class LocalStorageService(StorageService):

    def upload(
        self,
        file,
        folder
    ):

        return save_file(
            file,
            folder
        )

    def delete(
        self,
        folder,
        filename
    ):

        delete_file(
            folder,
            filename
        )

    def download(
        self,
        folder,
        filename,
        download_name=None
    ):

        return send_from_directory(
            folder,
            filename,
            as_attachment=True,
            download_name=download_name
        )

    def exists(
        self,
        folder,
        filename
    ):

        return os.path.exists(
            os.path.join(
                folder,
                filename
            )
        )
    def get_download_url(
    self,
    folder,
    filename,
    expiry=300
):

        return None
    
    def get_upload_url(
    self,
    filename,
    folder,
    content_type,
    expiry=300
):
        return None