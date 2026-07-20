import json
import logging

from flask import (
    has_request_context,
    request,
    g
)
class JsonFormatter(
    logging.Formatter
):

    def format(
        self,
        record
    ):

        log = {

            "timestamp":
                self.formatTime(
                    record
                ),

            "level":
                record.levelname,

            "message":
                record.getMessage()
        }
        if has_request_context():

            log["path"] = (
                request.path
            )

            log["method"] = (
                request.method
            )

            log["request_id"] = (
                getattr(
                    g,
                    "request_id",
                    None
                )
            )

            log["user_id"] = (
                getattr(
                    g,
                    "user_id",
                    None
                )
            )
        return json.dumps(
            log
        )