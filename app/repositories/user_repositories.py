from app.exceptions import user_exception
from app.models import User
from app.extensions import db
from app.logging_config import logger




def get_user_by_email(email):
    return User.query.filter_by(
        email=email
    ).first()


def get_user_by_id(user_id):
    user= User.query.get(user_id)
    if not user:
       logger.warning(f"User not found: ID {user_id}")
       raise user_exception.UserNotFoundException()
    return user


def get_all_users():
    return User.query.all()