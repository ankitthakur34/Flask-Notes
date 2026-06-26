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

