
from app.models.user_model import User
from app.extensions import db


def create_user(data):
    user = User(
        username=data.get('username'),
        email=data.get('email'),
    )
    db.session.add(user)
    db.session.commit()
    
    return user

def get_all_users():
    users = User.query.all()

    return [user.to_dict() for user in users]

def get_user_notes(user_id):
    user = User.query.get(user_id)
    if user:
        return user.notes
    return None

def get_user_notes2(user_id):

    user = User.query.get(user_id)

    if not user:
        return None

    return [note.to_dict() for note in user.notes]