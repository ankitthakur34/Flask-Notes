import logging


class RequestFilter(logging.Filter):

    def filter(self, record):

        return (
            getattr(
                record,
                "log_type",
                None
            )
            ==
            "request"
        )


class ErrorFilter(logging.Filter):

    def filter(self, record):

        return (
            record.levelno >= logging.ERROR
        )


class AppFilter(logging.Filter):

    def filter(self, record):

        message = record.getMessage()

        return (
            "REQUEST" not in message
            and
            "RESPONSE" not in message
            and
            record.levelno < logging.ERROR
        )