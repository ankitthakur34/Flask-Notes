import logging
import os

from logging.handlers import (
    RotatingFileHandler
)

from app.logging.filters import (
    RequestFilter,
    ErrorFilter,
    AppFilter
)
from app.logging.formatters import (
    JsonFormatter
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

    logger.propagate = False

    # Flask debug reload imports twice
    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )
    json_formatter = (
    JsonFormatter()
)

    # ==========================
    # APP LOGS
    # ==========================

    app_handler = (
        RotatingFileHandler(
            "logs/app.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=5
        )
    )

    app_handler.setLevel(
        logging.INFO
    )

    app_handler.setFormatter(
        json_formatter
    )

    app_handler.addFilter(
        AppFilter()
    )

    # ==========================
    # ERROR LOGS
    # ==========================

    error_handler = (
        RotatingFileHandler(
            "logs/error.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=5
        )
    )

    error_handler.setLevel(
        logging.ERROR
    )

    error_handler.setFormatter(
        json_formatter
    )

    error_handler.addFilter(
        ErrorFilter()
    )

    # ==========================
    # REQUEST LOGS
    # ==========================

    request_handler = (
        RotatingFileHandler(
            "logs/request.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=5
        )
    )

    request_handler.setLevel(
        logging.INFO
    )

    request_handler.setFormatter(
        json_formatter
    )

    request_handler.addFilter(
        RequestFilter()
    )

    # ==========================
    # CONSOLE
    # ==========================

    console_handler = (
        logging.StreamHandler()
    )

    console_handler.setLevel(
        logging.INFO
    )

    console_handler.setFormatter(
        formatter
    )

    # ==========================
    # ADD HANDLERS
    # ==========================

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

    return logger


logger = configure_logger()