from abc import ABC, abstractmethod


class StorageService(ABC):

    @abstractmethod
    def upload(
        self,
        file,
        folder
    ):
        pass

    @abstractmethod
    def delete(
        self,
        folder,
        filename
    ):
        pass

    @abstractmethod
    def download(
        self,
        folder,
        filename,
        download_name=None  
    ):
        pass

    @abstractmethod
    def exists(
        self,
        folder,
        filename
    ):
        pass
    @abstractmethod

    def get_download_url(
    self,
    folder,
    filename,
    expiry=300
):
        pass

    @abstractmethod
    def get_upload_url(
    self,
    filename,
    folder,
    content_type,
    expiry=300
):
        pass