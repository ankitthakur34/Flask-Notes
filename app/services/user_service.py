
from app.exceptions import user_exception
from app.models.user_model import User
from app.extensions import db
from app.repositories import user_repositories
from app.logging_config import logger



def get_all_users():
    users = user_repositories.get_all_users()

    return [user.to_dict() for user in users]

def get_user_notes(user_id):
    user = user_repositories.get_user_by_id(user_id)
    
    
    return user.notes

def get_user_by_id(user_id):
    user = user_repositories.get_user_by_id(user_id)
    
    return user
    

