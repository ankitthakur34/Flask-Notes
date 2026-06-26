from app.exceptions import auth_exception
from app.models import User
from app.extensions import db
from app.utils import generate_verification_token,verify_verification_token,send_verification_email,send_reset_email,verify_reset_token,generate_reset_token
from app.logging_config import logger
from app.tasks import send_email_task

from app.repositories.user_repositories import get_user_by_email,get_user_by_id



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
    send_email_task.delay(
    user.email,
    "Verify Your Email",
    f"""
    Click the link below:

    {verification_url}
    """
)

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

def forgot_password(email):

    user = get_user_by_email(email)

    if user:

        token = generate_reset_token(
            user.id
        )

        reset_url = (
            f"http://localhost:5000"
            f"/reset-password/{token}"
        )

        send_email_task.delay(
    user.email,
    "Reset Password",
    f"""
    Click the link below:

    {reset_url}
    """
)

    return {
        "message":
        "If the email exists, a reset link has been sent"
    }
def reset_password(
    token,
    new_password
):

    user_id = verify_reset_token(
        token
    )

    if not user_id:

        return None

    user = get_user_by_id(
        user_id
    )

    if not user:

        return None

    user.set_password(
        new_password
    )

    db.session.commit()

    return user