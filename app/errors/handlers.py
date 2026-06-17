
from marshmallow import Schema, fields,validates, ValidationError
from flask import jsonify
from app.exceptions import auth_exception, user_exception, note_exception
from app.utils import success_response, error_response
from app.exceptions.rateLimit_exception import RateLimitException
from app.logging_config import logger

def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation(error):

        return error_response(
        error.message,
        404
    )
    
    @app.errorhandler(note_exception.NoteNotFoundException)
    def handle_note_not_found(error):

         return error_response(
        error.message,
        error.status_code
    )
    
    @app.errorhandler(auth_exception.InvalidCredentialsException)
    def handle_auth_exception(error):

        return error_response(
        error.message,
        error.status_code
    )
    
    @app.errorhandler(user_exception.UserNotFoundException)
    def handle_user_not_found(error):

        return error_response(
        error.message,
        error.status_code
    )
    @app.errorhandler(auth_exception.ForbiddenException)
    def handle_forbidden(error):

        return error_response(
        error.message,
        error.status_code
    )
    @app.errorhandler(RateLimitException)
    def handle_rate_limit(error):

        return error_response(
        error.message,
        error.status_code
    )
    @app.errorhandler(auth_exception.EmailNotVerified)
    def handle_usernotverified(error):
        return error_response(
        error.message,
        error.status_code
    )

    