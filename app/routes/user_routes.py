from flask import Blueprint, request

from app.exceptions import user_exception
from app.repositories import user_repositories
from app.services.user_service import (
    get_all_users,
    get_user_notes
)
from app.exceptions import user_exception
from app.logging_config import logger


user_bp = Blueprint(
    "user_bp",
    __name__
)



@user_bp.route("/users", methods=["GET"])
def get_users_route():

    users = get_all_users()

    return {
        "data": users
    }, 200

@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_route(user_id):

    user = user_repositories.get_user_by_id(user_id)
    logger.info(f"Fetching user: {user}")
    if not user:
       raise user_exception.UserNotFoundException()

    return {
        "data": user.to_dict()
    }, 200

@user_bp.route("/users/<int:user_id>/notes", methods=["GET"])
def get_user_notes_route(user_id):

    notes = get_user_notes(user_id)

    if notes is None:
        raise user_exception.UserNotFoundException()

    return {
        'notes': [note.to_dict() for note in notes]
    },200