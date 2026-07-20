import logging
import os

from logging.handlers import (
    RotatingFileHandler
)


def configure_logger():

    os.makedirs(
        "logs",
        exist_ok=True
    )

    logger = logging.getLogger(
        "notes_app"
    )

    logger.setLevel(
        logging.INFO
    )

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )

    app_handler = (
        RotatingFileHandler(
            "logs/app.log",
            maxBytes=
            10 * 1024 * 1024,
            backupCount=5
        )
    )

    app_handler.setFormatter(
        formatter
    )

    error_handler = (
        RotatingFileHandler(
            "logs/error.log",
            maxBytes=
            10 * 1024 * 1024,
            backupCount=5
        )
    )

    error_handler.setLevel(
        logging.ERROR
    )

    error_handler.setFormatter(
        formatter
    )

    request_handler = (
        RotatingFileHandler(
            "logs/request.log",
            maxBytes=
            10 * 1024 * 1024,
            backupCount=5
        )
    )

    request_handler.setFormatter(
        formatter
    )

    console_handler = (
        logging.StreamHandler()
    )

    console_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        app_handler
    )

    logger.addHandler(
        error_handler
    )

    logger.addHandler(
        request_handler
    )

    logger.addHandler(
        console_handler
    )
    print(logger.handlers)
    print(os.getcwd())
    print(
    os.path.getsize(
        "logs/app.log"
    )
)

    return logger


logger = (
    configure_logger()
)