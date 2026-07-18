import boto3
import uuid
import os

from flask import current_app

from app.storage.storage_service import (
    StorageService
)
from botocore.exceptions import (
    ClientError
)
from io import BytesIO
from flask import send_file

class S3StorageService(
    StorageService
):

    def __init__(self):

        self.bucket = current_app.config[
            "AWS_BUCKET_NAME"
        ]

        self.client = boto3.client(
            "s3",
            aws_access_key_id=current_app.config[
                "AWS_ACCESS_KEY_ID"
            ],
            aws_secret_access_key=current_app.config[
                "AWS_SECRET_ACCESS_KEY"
            ],
            region_name=current_app.config[
                "AWS_REGION"
            ]
        )

    def delete(
    self,
    folder,
    filename
):

        key = (
        f"{folder}/"
        f"{filename}"
    )

        self.client.delete_object(
        Bucket=self.bucket,
        Key=key
    )

    def upload(
    self,
    file,
    folder
):

        extension = os.path.splitext(
        file.filename
    )[1]

        filename = (
        f"{uuid.uuid4()}"
        f"{extension}"
    )

        key = (
        f"{folder}/"
        f"{filename}"
    )

        self.client.upload_fileobj(
        file,
        self.bucket,
        key,
        ExtraArgs={
            "ContentType":
            file.content_type
        }
    )

        return filename 

    def exists(
    self,
    folder,
    filename
):

        key = (
        f"{folder}/"
        f"{filename}"
    )

        try:

            self.client.head_object(
            Bucket=self.bucket,
            Key=key
        )

            return True

        except ClientError:

            return False   
    def download(
    self,
    folder,
    filename,
    download_name=None
):

        key = (
        f"{folder}/"
        f"{filename}"
    )

        try:

            response = self.client.get_object(
            Bucket=self.bucket,
            Key=key
        )

        except ClientError:

            raise FileNotFoundError(
            "File not found in S3."
        )

        file_stream = BytesIO(
        response["Body"].read()
    )

        return send_file(
        file_stream,
        mimetype=response[
            "ContentType"
        ],
        as_attachment=True,
        download_name=(
            download_name
            or filename
        )
    )

    def get_download_url(
    self,
    folder,
    filename,
    expiry=300
):

        key = (
        f"{folder}/"
        f"{filename}"
    )

        return self.client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": self.bucket,
            "Key": key
        },
        ExpiresIn=expiry
    )

    def get_upload_url(
    self,
    filename,
    folder,
    content_type,
    expiry=300
):

        extension = os.path.splitext(
        filename
    )[1]

        generated_filename = (
        f"{uuid.uuid4()}"
        f"{extension}"
    )

        key = (
        f"{folder}/"
        f"{generated_filename}"
    )

        url = (
        self.client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self.bucket,
                "Key": key,
                "ContentType": content_type
            },
            ExpiresIn=expiry
        )
    )

        return {
        "upload_url": url,
        "filename": generated_filename,
        "key": key
    }

    def initiate_multipart_upload(
    self,
    filename,
    folder,
    content_type
):

        extension = os.path.splitext(
        filename
    )[1]

        generated_filename = (
        f"{uuid.uuid4()}"
        f"{extension}"
    )

        key = (
        f"{folder}/"
        f"{generated_filename}"
    )

        response = (
        self.client.create_multipart_upload(
            Bucket=self.bucket,
            Key=key,
            ContentType=content_type
        )
    )

        return {
        "upload_id":
            response["UploadId"],

        "filename":
            generated_filename,

        "key":
            key
    }


    def get_part_upload_url(
    self,
    filename,
    folder,
    upload_id,
    part_number
):

        key = (
        f"{folder}/"
        f"{filename}"
    )

        url = (
        self.client.generate_presigned_url(
            ClientMethod="upload_part",
            Params={
                "Bucket":
                    self.bucket,

                "Key":
                    key,

                "UploadId":
                    upload_id,

                "PartNumber":
                    part_number
            },
            ExpiresIn=3600
        )
    )

        return {
        "upload_url": url,
        "part_number": part_number
    }


    def complete_multipart_upload(
    self,
    filename,
    folder,
    upload_id,
    parts
):

        key = (
        f"{folder}/"
        f"{filename}"
    )

        response = (
        self.client.complete_multipart_upload(
            Bucket=self.bucket,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={
                "Parts": parts
            }
        )
    )

        return {
        "location":
            response.get("Location"),

        "key":
            response.get("Key"),

        "etag":
            response.get("ETag")
    }


    def abort_multipart_upload(
    self,
    filename,
    folder,
    upload_id
):

        key = (
        f"{folder}/"
        f"{filename}"
    )

        self.client.abort_multipart_upload(
        Bucket=self.bucket,
        Key=key,
        UploadId=upload_id
    )

        return True
    
    def list_uploaded_parts(
    self,
    filename,
    folder,
    upload_id
):

        key = (
        f"{folder}/"
        f"{filename}"
    )

        response = (
        self.client.list_parts(
            Bucket=self.bucket,
            Key=key,
            UploadId=upload_id
        )
    )

        parts = []

        for part in response.get(
        "Parts",
        []
    ):

            parts.append(
            {
                "part_number":
                    part["PartNumber"],

                "etag":
                    part["ETag"],

                "size":
                    part["Size"]
            }
        )

        return parts