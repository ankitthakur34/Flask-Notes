from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()



class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')    
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    DEBUG = True if os.getenv('FLASK_ENV') == 'development' else False

    MAIL_SERVER = "smtp.gmail.com"

    MAIL_PORT = 587

    MAIL_USE_TLS = True

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")

    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    MAIL_DEFAULT_SENDER = (
    os.getenv("MAIL_USERNAME")
)
    CELERY_BROKER_URL = (
    "redis://localhost:6379/0"
    )

    CELERY_RESULT_BACKEND = (
    "redis://localhost:6379/0"
    )

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    UPLOAD_FOLDER = os.path.join(
    os.getcwd(),
    "uploads"
)

    PROFILE_UPLOAD_FOLDER = os.path.join(
    UPLOAD_FOLDER,
    "profile"
)
    ATTACHMENT_UPLOAD_FOLDER = os.path.join(
    UPLOAD_FOLDER,
    "attachments"
)
    ATTACHMENT_FOLDER = "attachments"
    PROFILE_FOLDER = "profile"
    PROFILE_S3_FOLDER = "profile"

    ATTACHMENT_S3_FOLDER = "attachments"

    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    MAX_FILE_SIZE = 5 * 1024 * 1024
    MAX_ATTACHMENT_SIZE = 5 * 1024 * 1024

    ALLOWED_IMAGE_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}
    ALLOWED_ATTACHMENT_EXTENSIONS = {
    "pdf",
    "doc",
    "docx",
    "ppt",
    "pptx",
    "xls",
    "xlsx",
    "jpg",
    "jpeg",
    "png",
    "webp",
    "txt",
    "csv",
    "zip"
}
    
    ALLOWED_IMAGE_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp"
}
    
    ALLOWED_ATTACHMENT_MIME_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/plain",
    "text/csv",
    "application/zip",
    "image/jpeg",
    "image/png",
    "image/webp"
}
    AWS_ACCESS_KEY_ID = os.getenv(
    "AWS_ACCESS_KEY_ID"
)

    AWS_SECRET_ACCESS_KEY = os.getenv(
    "AWS_SECRET_ACCESS_KEY"
)

    AWS_REGION = os.getenv(
    "AWS_REGION"
)

    AWS_BUCKET_NAME = os.getenv(
    "AWS_BUCKET_NAME"
)
    
    UPLOAD_PROVIDER = "S3"

