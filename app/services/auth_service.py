from app.exceptions import auth_exception
from app.models import User
from app.extensions import db
from app.utils import generate_verification_token,verify_verification_token,send_verification_email
from app.logging_config import logger



def register_user(data):

    user = User(
        username=data["username"],
        email=data["email"],
        is_verified=False
    )

    user.set_password(data["password"])

    

    db.session.add(user)
    db.session.commit()

    token = generate_verification_token(user.id)

    verification_url= (
    f"http://localhost:5000"
    f"/verify-email/{token}"
)
    logger.info(
    f"Verification URL: {verification_url}"
)
    send_verification_email(user.email,verification_url)

    return user


def login_user(data):

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        raise auth_exception.InvalidCredentialsException()

    if not user.check_password(data["password"]):
        raise auth_exception.InvalidCredentialsException()
    if not user.is_verified:

        raise auth_exception.EmailNotVerified()

    return user