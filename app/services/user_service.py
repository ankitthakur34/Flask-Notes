
from app.exceptions import user_exception,BadRequestException
from app.models.user_model import User
from app.extensions import db
from app.repositories import user_repositories
from app.logging import logger

from flask import current_app
from app.utils import error_response,success_response
from app.utils.file_util import allowed_extension,allowed_mime_type,save_file,delete_file,verify_image




def get_all_users():
    users = user_repositories.get_all_users()

    return [user.to_dict() for user in users]

def get_user_notes(user_id):
    user = user_repositories.get_user_by_id(user_id)
    
    
    return user.notes

def get_user_by_id(user_id):
    user = user_repositories.get_user_by_id(user_id)
    
    return user




def upload_profile_image(user_id,image):

    user = get_user_by_id(user_id)

    if image.filename == "":
          raise BadRequestException(
            "Only JPG, JPEG, PNG and WEBP are allowed."
        )
    
    if not allowed_extension(image.filename,current_app.config["ALLOWED_IMAGE_EXTENSIONS"]):
        raise BadRequestException("Invalid file extension")


    if not allowed_mime_type(image,current_app.config["ALLOWED_IMAGE_MIME_TYPES"]):
        raise BadRequestException("Invalid MIME type")


    if not verify_image(image):
        raise BadRequestException("Invalid image")
  
    
    if user.profile_image:

        delete_file(
            current_app.config[
        "PROFILE_UPLOAD_FOLDER"
    ],
    user.profile_image
        )
        

    filename = save_file(
         image,
    current_app.config[
        "PROFILE_UPLOAD_FOLDER"
    ]
    )

    user.profile_image = filename

    db.session.commit()

    return user
    

