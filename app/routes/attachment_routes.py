from flask import Blueprint

from flask import request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from flask import (
    current_app,
    send_from_directory
)
from app.dto import AttachmentDTO
from app.storage import get_storage
from app.services.attachment_service import upload_attachments,get_note_attachments,get_attachment,delete_attachment,replace_attachment
from app.utils.api_respone import success_response

attachment_bp = Blueprint(
    "attachments",
    __name__,
    url_prefix="/attachments"
)

@attachment_bp.route("/notes/<int:note_id>", methods=["POST"])
@jwt_required()
def upload_note_attachments(note_id):

    files = request.files.getlist("files")

    attachments = upload_attachments(
        note_id,
        get_jwt_identity(),
        files
    )

    return success_response(
        data=AttachmentDTO.to_list(
    attachments
),
        message="Attachments uploaded successfully",
        status_code=201
    )


@attachment_bp.route(
    "/notes/<int:note_id>",
    methods=["GET"]
)
@jwt_required()
def get_attachments(note_id):

    attachments = get_note_attachments(
        note_id,
        get_jwt_identity()
    )

    return success_response(
        data=AttachmentDTO.to_list(
    attachments
),
        message="Attachments fetched successfully"
    )

@attachment_bp.route(
    "/<int:attachment_id>/download",
    methods=["GET"]
)
@jwt_required()
def download_attachment(
    attachment_id
):

    attachment = get_attachment(
        attachment_id,
        get_jwt_identity()
    )
    storage=get_storage()

    return storage.download(
        current_app.config[
            "ATTACHMENT_UPLOAD_FOLDER"
        ],
        attachment.filename,
       attachment.original_filename
    )

@attachment_bp.route(
    "/<int:attachment_id>",
    methods=["DELETE"]
)
@jwt_required()
def remove_attachment(
    attachment_id
):

    delete_attachment(
        attachment_id,
        get_jwt_identity()
    )

    return success_response(
        data=[],
        message="Attachment deleted successfully"
    )


@attachment_bp.route(
    "/<int:attachment_id>",
    methods=["PUT"]
)
@jwt_required()
def replace_attachment_route(
    attachment_id
):

    file = request.files.get("file")

    attachment = replace_attachment(
        attachment_id,
        get_jwt_identity(),
        file
    )

    return success_response(
        data=AttachmentDTO.to_response(
    attachment
),
        message="Attachment replaced successfully"
    )