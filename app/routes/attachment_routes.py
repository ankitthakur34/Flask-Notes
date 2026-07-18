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
from app.exceptions import note_exception
from app.storage import get_storage
from app.services.attachment_service import list_uploaded_parts,get_in_progress_uploads,mark_part_uploaded,get_uploaded_parts, abort_multipart_attachment,complete_multipart_attachment,get_multipart_part_url,upload_attachments,get_note_attachments,get_attachment,delete_attachment,replace_attachment,complete_presigned_upload,initiate_multipart_upload
from app.services.note_service import get_note_by_id
from app.utils.api_respone import success_response
from app.dto.attachment_dto import AttachmentDTO
from app.storage.factory import (
    get_attachment_folder
)

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
    "/upload-url",
    methods=["POST"]
)
@jwt_required()
def generate_upload_url():

    data = request.get_json()

    note_id = data.get(
        "note_id"
    )

    filename = data.get(
        "filename"
    )

    content_type = data.get(
        "content_type"
    )

    note = get_note_by_id(note_id,get_jwt_identity())

    if not note:
        raise note_exception.NoteNotFoundException(
            "Note not found."
        )

    storage = get_storage()

    response = (
        storage.get_upload_url(
            filename=filename,
            folder=get_attachment_folder(),
            content_type=content_type
        )
    )

    response["note_id"] = note_id

    return success_response(
        data=response,
        message="Upload URL generated"
    )


@attachment_bp.route(
    "/complete-upload",
    methods=["POST"]
)
@jwt_required()
def complete_upload():

    data = request.get_json()

    attachment = (
        complete_presigned_upload(
            note_id=data[
                "note_id"
            ],
            user_id=
            get_jwt_identity(),
            filename=data[
                "filename"
            ],
            original_filename=data[
                "original_filename"
            ],
            mime_type=data[
                "mime_type"
            ],
            file_size=data[
                "file_size"
            ]
        )
    )

    return success_response(
        data=
        AttachmentDTO.to_response(
            attachment
        ),
        message=
        "Attachment saved."
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

    storage = get_storage()

    if current_app.config[
        "UPLOAD_PROVIDER"
    ] == "S3":

        url = storage.get_download_url(
            get_attachment_folder(),
            attachment.filename,
            expiry=300
        )

        return success_response(
            data={
                "download_url": url,
                "expires_in": 300
            },
            message=(
                "Presigned URL generated"
            )
        )
    print("defualt download method")
    return storage.download(
        get_attachment_folder(),
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


@attachment_bp.route(
    "/multipart/initiate",
    methods=["POST"]
)
@jwt_required()
def initiate_multipart_route():

    data = request.get_json()

    note_id = data.get(
        "note_id"
    )

    filename = data.get(
        "filename"
    )

    content_type = data.get(
        "content_type"
    )
    total_parts= data.get("total_parts")

    response = (
        initiate_multipart_upload(
            note_id,
            get_jwt_identity(),
            filename,
            content_type,
            total_parts
        )
    )

    return success_response(
        data=response,
        message=(
            "Multipart upload initiated"
        )
    )

@attachment_bp.route(
    "/multipart/part-url",
    methods=["POST"]
)
@jwt_required()
def multipart_part_url():

    data = request.get_json()

    filename = data.get(
        "filename"
    )

    upload_id = data.get(
        "upload_id"
    )

    part_number = data.get(
        "part_number"
    )

    response = (
        get_multipart_part_url(
            get_jwt_identity(),
            filename,
            upload_id,
            part_number
        )
    )

    return success_response(
        data=response,
        message=(
            "Part upload URL generated."
        )
    )


@attachment_bp.route(
    "/multipart/complete",
    methods=["POST"]
)
@jwt_required()
def complete_multipart_route():

    data = request.get_json()

    attachment = (
        complete_multipart_attachment(
            note_id=data["note_id"],
            user_id=get_jwt_identity(),
            filename=data["filename"],
            upload_id=data["upload_id"],
            parts=data["parts"],
            original_filename=data[
                "original_filename"
            ],
            content_type=data[
                "content_type"
            ],
            file_size=data[
                "file_size"
            ]
        )
    )

    return success_response(
        data=AttachmentDTO.to_response(
            attachment
        ),
        message=(
            "Multipart upload completed."
        )
    )

@attachment_bp.route(
    "/multipart/abort",
    methods=["DELETE"]
)
@jwt_required()
def abort_multipart_route():

    data = request.get_json()

    abort_multipart_attachment(
        user_id=get_jwt_identity(),
        filename=data["filename"],
        upload_id=data["upload_id"]
    )

    return success_response(
        data=[],
        message="Multipart upload aborted."
    )

@attachment_bp.route(
    "/multipart/parts",
    methods=["POST"]
)
@jwt_required()
def uploaded_parts_route():

    data = request.get_json()

    parts = (
        get_uploaded_parts(
            filename=data[
                "filename"
            ],
            upload_id=data[
                "upload_id"
            ]
        )
    )

    return success_response(
        data=parts,
        message=(
            "Uploaded parts fetched."
        )
    )


@attachment_bp.route(
    "/multipart/part-success",
    methods=["POST"]
)
@jwt_required()
def multipart_part_uploaded():

    data = request.get_json()

    upload = mark_part_uploaded(
        upload_id=data["upload_id"],
        part_number=data["part_number"]
    )

    return success_response(
        data={
            "uploaded_parts":
            upload.uploaded_part_numbers
        },
        message="Part marked uploaded."
    )

@attachment_bp.route(
    "/multipart/in-progress",
    methods=["GET"]
)
@jwt_required()
def get_uploads():

    uploads = (
        get_in_progress_uploads(
            get_jwt_identity()
        )
    )

    return success_response(
        data=[
            AttachmentDTO.multipart_to_response(
                u
            )
            for u in uploads
        ]
    )

@attachment_bp.route(
    "/multipart/list-parts",
    methods=["POST"]
)
@jwt_required()
def multipart_list_parts():

    data = request.get_json()

    parts = (
        list_uploaded_parts(
            upload_id=data["upload_id"],
            filename=data["filename"]
        )
    )

    return success_response(
        data=parts,
        message="Parts fetched successfully."
    )