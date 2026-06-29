from flask import Blueprint, request

from app.decoraters import role_required
from app.exceptions import user_exception
from app.repositories import user_repositories
from app.services.user_service import (
    get_all_users,
    get_user_notes,
    get_user_by_id
)
from app.exceptions import user_exception,BadRequestException
from app.logging_config import logger
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import success_response, error_response
from app.services.user_service import upload_profile_image
from app.models.user_model import User
from flask import send_from_directory, current_app



user_bp = Blueprint(
    "user_bp",
    __name__
)



@user_bp.route("/users", methods=["GET"])
@role_required("ADMIN")
def get_users_route():

    users = get_all_users()
    logger.info(f"Fetching all users: {len(users)} users found")
    return {
        "data": users
    }, 200

@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_route(user_id):

    user = get_user_by_id(user_id)
    logger.info(f"Fetching user: {user}")
    
    logger.info(f"User retrieved: {user.username} with email: {user.email}")
    return {
        "data": user.to_dict()
    }, 200

@user_bp.route("/users/<int:user_id>/notes", methods=["GET"])
def get_user_notes_route(user_id):

    notes = get_user_notes(user_id)

    logger.info(f"Fetching notes for user_id: {user_id} - {len(notes)} notes found")

    return {
        'notes': [note.to_dict() for note in notes]
    },200

@user_bp.route("/upload-profile_image",methods=["POST"])
@jwt_required()
def upload_image():

    user_id =get_jwt_identity()
    

    if "image" not in request.files:

        return error_response(
            "Image is required"
        )

    image = request.files["image"]

    user= upload_profile_image(
        user_id,
        image
    )

    return success_response(
        data=user.to_dict(),
        message="Profile image uploaded"
    )

@user_bp.route("/profile-image/<filename>",methods=["GET"]
)
def get_profile_image(filename):

    return send_from_directory(
        current_app.config["PROFILE_UPLOAD_FOLDER"],
        filename
    )

