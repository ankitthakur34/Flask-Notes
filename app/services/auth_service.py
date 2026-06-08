from app.models import User
from app.extensions import db


def register_user(data):

    user = User(
        username=data["username"],
        email=data["email"]
    )

    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return user


def login_user(data):

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return None

    if not user.check_password(data["password"]):
        return None

    return user