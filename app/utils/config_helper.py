from flask import current_app

from app.logging.masker import (
    mask_sensitive_data
)


def get_safe_config(app):

    return (
        mask_sensitive_data(
            dict(
                app.config
            )
        )
    )