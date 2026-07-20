from functools import wraps
from flask import request

from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt_identity
)

from app.extensions import redis_client

from app.exceptions.rateLimit_exception import RateLimitException
from app.logging import logger

def rate_limit(max_requests,window_seconds):

    def wrapper(fn):

        @wraps(fn)
        def decorator(*args, **kwargs):

            verify_jwt_in_request()

            user_id = get_jwt_identity()

            key = (
                f"rate_limit:{user_id}:{request.method}:{request.endpoint}"
            )

            current_count = redis_client.get(key)
            logger.info(f"Rate limit check for user_id: {user_id} - current count: {current_count}")

            if current_count:

                current_count = int(
                    current_count
                )

                if current_count >= max_requests:

                    raise RateLimitException()

                redis_client.incr(key)

            else:

                redis_client.setex(
                    key,
                    window_seconds,
                    1
                )

            return fn(
                *args,
                **kwargs
            )

        return decorator

    return wrapper