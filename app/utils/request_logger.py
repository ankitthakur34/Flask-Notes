from flask import request
from app.logging_config import logger


def log_request():

    logger.info(
        f"REQUEST | "
        f"Method={request.method} | "
        f"Path={request.path}"
    )


def log_response(response):

    logger.info(
        f"RESPONSE | "
        f"Status={response.status_code}"
    )

    return response