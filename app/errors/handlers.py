import traceback

from marshmallow import ValidationError

from app.exceptions import (
    auth_exception,
    user_exception,
    note_exception,
    BadRequestException
)

from app.exceptions.rateLimit_exception import (
    RateLimitException
)

from app.utils import (
    error_response
)

from app.logging import logger


def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation(error):

        logger.warning(
            f"Validation Error : "
            f"{error.messages}"
        )

        return error_response(
            error.messages,
            400
        )

    @app.errorhandler(
        note_exception.NoteNotFoundException
    )
    def handle_note_not_found(error):

        logger.warning(
            f"Note Not Found : "
            f"{error.message}"
        )

        return error_response(
            error.message,
            error.status_code
        )

    @app.errorhandler(
        auth_exception.InvalidCredentialsException
    )
    def handle_auth_exception(error):

        logger.warning(
            f"Invalid Credentials : "
            f"{error.message}"
        )

        return error_response(
            error.message,
            error.status_code
        )

    @app.errorhandler(
        user_exception.UserNotFoundException
    )
    def handle_user_not_found(error):

        logger.warning(
            f"User Not Found : "
            f"{error.message}"
        )

        return error_response(
            error.message,
            error.status_code
        )

    @app.errorhandler(
        auth_exception.ForbiddenException
    )
    def handle_forbidden(error):

        logger.warning(
            f"Forbidden : "
            f"{error.message}"
        )

        return error_response(
            error.message,
            error.status_code
        )

    @app.errorhandler(
        RateLimitException
    )
    def handle_rate_limit(error):

        logger.warning(
            f"Rate Limit : "
            f"{error.message}"
        )

        return error_response(
            error.message,
            error.status_code
        )

    @app.errorhandler(
        auth_exception.EmailNotVerified
    )
    def handle_user_not_verified(error):

        logger.warning(
            f"Email Not Verified : "
            f"{error.message}"
        )

        return error_response(
            error.message,
            error.status_code
        )

    @app.errorhandler(
        BadRequestException
    )
    def handle_bad_request(error):

        logger.warning(
            f"Bad Request : "
            f"{error.message}"
        )

        return error_response(
            error.message,
            error.status_code
        )

    # Catch all unhandled exceptions
    @app.errorhandler(Exception)
    def handle_internal_error(error):

        

        logger.exception(
    "Unhandled Exception"
)

        return error_response(
            "Internal Server Error",
            500
        )