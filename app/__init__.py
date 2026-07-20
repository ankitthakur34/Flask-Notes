from flask import Flask
import os
from dotenv import load_dotenv
load_dotenv()

env = os.getenv(
    "APP_ENV",
    "development"
)

load_dotenv(
    f".env.{env}"
)
from flasgger import Swagger
from app.config import config_map



from app.routes import note_bp, user_bp,auth_bp,note_v2_bp,attachment_bp
from app.extensions import db,migrate,jwt,check_if_token_revoked,mail
from app.errors import register_error_handlers
from app.utils.request_logger import log_request, log_response
from app.swagger import swagger_config, swagger_template
from app.cache.token_cache import is_token_blacklisted
from app.backgroundJobs import make_celery
from app.logging import logger

from app.logging import (
    configure_logger
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(
    config_map[env]
)
    

    configure_logger(
    app.config[
        "LOG_LEVEL"
    ]
)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(note_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(note_v2_bp)
    app.register_blueprint(attachment_bp)
    register_error_handlers(app)
    app.before_request(log_request)
    app.after_request(log_response)
    Swagger(app, config=swagger_config, template=swagger_template)
    
    mail.init_app(app)
    celery = make_celery(app)

    app.celery = celery

    os.makedirs(
    app.config["PROFILE_UPLOAD_FOLDER"],
    exist_ok=True
)
    os.makedirs(
    app.config["ATTACHMENT_UPLOAD_FOLDER"],
    exist_ok=True
)
    


    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header,jwt_payload):

        jti = jwt_payload["jti"]

        return is_token_blacklisted(jti)
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header,jwt_payload):

        return {
        "success": False,
        "message": "Token has been revoked"
        }, 401
    
    logger.info(
    "=" * 50
)

    logger.info(
    f"Application Started "
    f"in "
    f"{app.config['ENV_NAME']}"
)

    logger.info(
    "=" * 50
)
    logger.info(
    f"Email Verification : "
    f"{app.config['REQUIRE_EMAIL_VERIFICATION']}"
)
    return app