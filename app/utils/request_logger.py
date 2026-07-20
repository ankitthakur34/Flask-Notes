import uuid
import time
from flask import current_app, request,g
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.logging import logger


def log_request():

    g.request_id = (
        str(uuid.uuid4())
    )

    g.start_time = (
        time.time()
    )
    g.client_ip = (
    request.remote_addr
)

    g.user_agent = (
    request.headers.get(
        "User-Agent"
    )
)

    g.environment = (
    current_app.config[
        "ENV_NAME"
    ]
)
    g.user_id = None

    try:

        verify_jwt_in_request(
            optional=True
        )

        g.user_id = (
            get_jwt_identity()
        )
    except Exception:
        pass

    logger.info(
    f"Incoming Request | "
    f"id={g.request_id} | "
    f"{request.method} "
    f"{request.path}"
)


def log_response(response):

    duration = round(

        (
            time.time()
            -
            g.start_time
        ) * 1000,
        2
    )
    g.duration = duration

    logger.info(
    f"Request Completed | "
    f"id={g.request_id} | "
    f"status={response.status_code} | "
    f"time={duration}ms"
)

    return response