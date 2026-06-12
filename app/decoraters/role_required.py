from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from app.exceptions import auth_exception

def role_required(role):

    def wrapper(fn):

        @wraps(fn)
        def decorator(*args, **kwargs):

            verify_jwt_in_request()

            claims = get_jwt()

            if claims.get("role") != role:
                raise auth_exception.ForbiddenException()

            return fn(*args, **kwargs)

        return decorator

    return wrapper
