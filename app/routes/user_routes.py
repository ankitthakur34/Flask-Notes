from flask import Blueprint, request

from app.services.user_service import (
    create_user,
    get_all_users,
    get_user_notes
)


user_bp = Blueprint(
    "user_bp",
    __name__
)


@user_bp.route("/users", methods=["POST"])
def create_user_route():

    data = request.get_json()

    user = create_user(data)

    return {
        "message": "User created",
        "data": user.to_dict()
    }, 201


@user_bp.route("/users", methods=["GET"])
def get_users_route():

    users = get_all_users()

    return {
        "data": users
    }, 200


@user_bp.route("/users/<int:user_id>/notes", methods=["GET"])
def get_user_notes_route(user_id):

    notes = get_user_notes(user_id)

    if notes is None:
        return {
            "message": "User not found"
        }, 404

    return {
        "data": notes
    }, 200