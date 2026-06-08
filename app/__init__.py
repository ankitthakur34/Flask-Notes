from flask import Flask

from app.config import Config
from app.routes import note_bp, user_bp,auth_bp
from app.extensions import db,migrate,jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(note_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    return app