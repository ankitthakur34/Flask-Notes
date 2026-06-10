from marshmallow import Schema, fields,validates, ValidationError
from flask import jsonify
from app.exceptions import auth_exception, user_exception, note_exception

def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation(err):

        return jsonify({
            "success": False,
            "errors": err.messages
        }),400
    @app.errorhandler(note_exception.NoteNotFoundException)
    def handle_note_not_found(err):

        return jsonify({
            "success": False,
            "error": "Note not found"
        }),404
    @app.errorhandler(auth_exception.InvalidCredentialsException)
    def handle_auth_exception(err):

        return jsonify({
            "success": False,
            "error": "Authentication failed"
        }),401
    @app.errorhandler(user_exception.UserNotFoundException)
    def handle_user_not_found(err):

        return jsonify({
            "success": False,
            "error": "User not found"
        }),404
    