from flask import Flask
from flasgger import Swagger
from app.config import Config
from app.routes import note_bp, user_bp,auth_bp,note_v2_bp
from app.extensions import db,migrate,jwt,check_if_token_revoked,mail
from app.errors import register_error_handlers
from app.utils.request_logger import log_request, log_response
from app.swagger import swagger_config, swagger_template
from app.cache.token_cache import is_token_blacklisted
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(note_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(note_v2_bp)
    register_error_handlers(app)
    app.before_request(log_request)
    app.after_request(log_response)
    Swagger(app, config=swagger_config, template=swagger_template)
    
    mail.init_app(app)


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
    return app