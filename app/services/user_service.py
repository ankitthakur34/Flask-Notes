
from app.models.user_model import User
from app.extensions import db
from app.repositories import user_repositories
from app.logging_config import logger



def get_all_users():
    users = user_repositories.get_all_users()

    return [user.to_dict() for user in users]

def get_user_notes(user_id):
    user = user_repositories.get_user_by_id(user_id)
    if user:
        return user.notes
    return None

def get_user_notes2(user_id):

    user = user_repositories.get_user_by_id(user_id)

    if not user:
        return None

    return [note.to_dict() for note in user.notes]