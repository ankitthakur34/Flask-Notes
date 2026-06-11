from marshmallow import Schema, fields,validates, ValidationError
from flask import jsonify
from app.exceptions import auth_exception, user_exception, note_exception
from app.utils import success_response, error_response

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
    