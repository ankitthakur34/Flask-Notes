from app.models import User
from app.extensions import db




def get_user_by_email(email):
    return User.query.filter_by(
        email=email
    ).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)



def get_all_users():
    return User.query.all()