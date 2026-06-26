from flask import Blueprint, request,current_app
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity,get_jwt
import jwt
from app.extensions import db

from app.services.auth_service import register_user, login_user,forgot_password,reset_password
from app.schemas import RegisterSchema,LoginSchema
from app.exceptions import auth_exception
from app.logging_config import logger
from app.repositories.user_repositories import get_user_by_email,get_user_by_id
from app.utils import success_response, error_response,generate_verification_token,verify_verification_token

from app.tasks import send_email_task

import time


from app.cache.token_cache import (
    blacklist_token
)



auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():

    
    data = RegisterSchema().load(request.get_json())
    
    user = register_user(data)

    logger.info(f"New user registered: {user.username} with email: {user.email}")

    return success_response(
        data=user.to_dict(),
        message="User registered successfully",
        status_code=201
    )

@auth_bp.route("/verify-email/<token>",methods=["GET"])
def verify_email(token):

    user_id = verify_verification_token(token)

    if not user_id:

        return error_response(
            message=
            "Invalid or expired token",
            status_code=400
        )

    user = get_user_by_id(user_id)

    if not user:

        return error_response(
            message="User not found",
            status_code=404
        )

    user.is_verified = True

    db.session.commit()

    return success_response(
        message=
        "Email verified successfully"
    )


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login
    ---
    tags:
      - Authentication

    parameters:
      - in: body
        name: body

        schema:
          type: object

          required:
            - email
            - password

          properties:

            email:
              type: string

            password:
              type: string

    responses:
      200:
        description: Login successful
    """

    data = LoginSchema().load(request.get_json())

    user = login_user(data)

    logger.info(f"User logged in: {user.username}")

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
        )
    refresh_token = create_refresh_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )
    return success_response(
        data={
            "access_token": token,
            "refresh_token": refresh_token
        },
        message="Login successful",
        status_code=200
    )


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():

    user_id = get_jwt_identity()

    new_access_token = create_access_token(
        identity=user_id
    )

    logger.info(f"Token refreshed for user: {user_id}")

    return success_response(
        data={
            "access_token": new_access_token
        },
        message="Token refreshed successfully",
        status_code=200
    )

@auth_bp.route('/logout',methods=['POST'])
@jwt_required()
def logout():
    token = get_jwt()

    jti = token["jti"]
    logger.info(
    f"Token blacklisted: {jti}"
)

    expires_in = (
        token["exp"]
        - int(time.time())
    )

    blacklist_token(
        jti,
        expires_in
    )
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    logger.info(f"Refresh Token : {refresh_token} ")
    if refresh_token:
        refresh_payload = jwt.decode(
            refresh_token,
            current_app.config[
                "JWT_SECRET_KEY"
            ],
            algorithms=["HS256"]
        )
        refresh_jti = refresh_payload["jti"]

        refresh_exp = (
            refresh_payload["exp"]
            - int(time.time())
        )
        blacklist_token(
            refresh_jti,
            refresh_exp
        )
    return success_response(
        message="Logout Scuccesfully"
    )

@auth_bp.route("/forgot-password",methods=["POST"])
def forgot_password_route():

    data = request.get_json()

    result = forgot_password(
        data["email"]
    )

    return success_response(
        message=result["message"]
    )

@auth_bp.route("/reset-password/<token>",methods=["POST"])
def reset_password_route( token):

    data = request.get_json()

    user = reset_password(
        token,
        data["password"]
    )

    if not user:

        return error_response(
            message=
            "Invalid or expired token",
            status_code=400
        )

    return success_response(
        message=
        "Password reset successfully"
    )

@auth_bp.route(
    "/test-task",
    methods=["GET"]
)
def test_task():

    send_email_task.delay(
        "ankit@gmail.com",
        "Test Subject",
        "Hello From Celery"
    )

    return {
        "message":
        "Task Queued Successfully"
    }, 200
    