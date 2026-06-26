from flask import current_app
from itsdangerous import URLSafeTimedSerializer,SignatureExpired,BadSignature

def generate_reset_token(user_id):

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    return serializer.dumps(
        user_id,
        salt="password-reset"
    )

def verify_reset_token(token, max_age=900):

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    try:

        return serializer.loads(
            token,
            salt="password-reset",
            max_age=max_age
        )

    except (
        SignatureExpired,
        BadSignature
    ):

        return None