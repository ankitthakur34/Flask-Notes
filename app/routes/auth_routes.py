from flask import Blueprint, request
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity

from app.services.auth_service import register_user, login_user
from app.schemas import RegisterSchema,LoginSchema
from app.exceptions import auth_exception

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():

    
    data = RegisterSchema().load(request.get_json())
    
    user = register_user(data)

    return {
        "message": "User created",
        "user": user.to_dict()
    }, 201


@auth_bp.route("/login", methods=["POST"])
def login():

    data = LoginSchema().load(request.get_json())

    user = login_user(data)

    if not user:
        raise auth_exception.InvalidCredentialsException()

    token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return {
        "access_token": token,
        "refresh_token": refresh_token
    }, 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():

    user_id = get_jwt_identity()

    new_access_token = create_access_token(
        identity=user_id
    )

    return {
        "access_token": new_access_token
    }, 200