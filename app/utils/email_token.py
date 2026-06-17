from flask import current_app
from itsdangerous import URLSafeTimedSerializer,SignatureExpired,BadSignature

def generate_verification_token(user_id):

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    return serializer.dumps(
        user_id,
        salt="email-verification"
    )

def verify_verification_token(token,max_age=3600):

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    try:

        user_id = serializer.loads(
            token,
            salt="email-verification",
            max_age=max_age
        )

        return user_id

    except (
        SignatureExpired,
        BadSignature
    ):

        return None