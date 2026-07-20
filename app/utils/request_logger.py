import uuid
import time
from flask import request,g
from app.logging import logger


def log_request():

    g.request_id = (
        str(uuid.uuid4())
    )

    g.start_time = (
        time.time()
    )

    logger.info(

        f"REQUEST | "
        f"id={g.request_id} | "
        f"method={request.method} | "
        f"path={request.path}"
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

    logger.info(

        f"RESPONSE | "
        f"id={g.request_id} | "
        f"status={response.status_code} | "
        f"time={duration}ms"
    )

    return response