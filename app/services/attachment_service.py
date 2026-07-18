from flask import current_app

from app.extensions import db
from app.models import Note, Attachment
from app.models import Note
from app.exceptions import (
    note_exception,
    BadRequestException
)
from app.models.multipart_upload_model import MultipartUpload
from app.storage import get_storage
from app.utils.file_util import (
    delete_file,
   calculate_checksum,
    validate_uploaded_file
)
from app.storage.factory import (
    get_attachment_folder
)



def upload_attachments(
    note_id,
    user_id,
    files
):
    """
    Upload multiple attachments for a note.
    """

    note = Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()

    if not note:
        raise note_exception.NoteNotFoundException("Note not found.")

    if not files:
        raise BadRequestException("No files uploaded.")
    
    storage=get_storage()


    uploaded_attachments = []
    saved_files = []

    try:

        for file in files:

            if file.filename == "":
                continue

            file_size = validate_uploaded_file(
    file=file,
    allowed_extensions=current_app.config[
        "ALLOWED_ATTACHMENT_EXTENSIONS"
    ],
    allowed_mime_types=current_app.config[
        "ALLOWED_ATTACHMENT_MIME_TYPES"
    ],
    verify_image_file=True,
    max_size=current_app.config[
        "MAX_ATTACHMENT_SIZE"
    ]
)
            checksum = calculate_checksum(file) 
       


            filename = storage.upload(
    file,
    get_attachment_folder()
)
            saved_files.append(filename)

            attachment = Attachment(
            filename=filename,
            original_filename=file.filename,
            file_path=filename,
            mime_type=file.content_type,
            file_size=file_size,
            note_id=note.id,
            checksum=checksum
        )

            db.session.add(attachment)

            uploaded_attachments.append(attachment)

        db.session.commit()

        return uploaded_attachments
    except Exception:
        db.session.rollback()
        for filename in saved_files:

           storage.delete(
    get_attachment_folder(),
    filename
)
        raise  





def get_note_attachments(
    note_id,
    user_id
):
    note = Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()

    if not note:
        raise note_exception.NoteNotFoundException(
            "Note not found."
        )

    return sorted(
    note.attachments,
    key=lambda attachment: attachment.created_at,
    reverse=True
)     


def get_attachment(
    attachment_id,
    user_id
):
    attachment = (
        Attachment.query
        .join(Note)
        .filter(
            Attachment.id == attachment_id,
            Note.user_id == user_id
        )
        .first()
    )

    if not attachment:
        raise note_exception.NoteNotFoundException(
            "Attachment not found."
        )

    return attachment


def delete_attachment(
    attachment_id,
    user_id
):

    attachment = (
        Attachment.query
        .join(Note)
        .filter(
            Attachment.id == attachment_id,
            Note.user_id == user_id
        )
        .first()
    )
    storage=get_storage()


    if not attachment:
        raise note_exception.NoteNotFoundException(
            "Attachment not found."
        )

    try:

        # Delete database row
        db.session.delete(attachment)

        db.session.commit()

        try:

           storage.delete(
    get_attachment_folder(),
    attachment.filename
)

        except Exception:

            current_app.logger.error(
        "Unable to delete attachment file: %s",
        attachment.filename
    )
       

    except Exception:

        db.session.rollback()

        raise

def replace_attachment(
    attachment_id,
    user_id,
    file
):

    attachment = (
        Attachment.query
        .join(Note)
        .filter(
            Attachment.id == attachment_id,
            Note.user_id == user_id
        )
        .first()
    )

    if not attachment:

        raise note_exception.NoteNotFoundException(
            "Attachment not found."
        )

    file_size = validate_uploaded_file(
        file=file,
        allowed_extensions=current_app.config[
            "ALLOWED_ATTACHMENT_EXTENSIONS"
        ],
        allowed_mime_types=current_app.config[
            "ALLOWED_ATTACHMENT_MIME_TYPES"
        ],
        verify_image_file=True,
        max_size=current_app.config[
            "MAX_ATTACHMENT_SIZE"
        ]
    )
    checksum = calculate_checksum(file)
    storage=get_storage()


    old_filename = attachment.filename

    new_filename = storage.upload(
    file,
    get_attachment_folder()
)

    attachment.filename = new_filename

    attachment.original_filename = file.filename

    attachment.file_path = new_filename

    attachment.mime_type = file.content_type

    attachment.file_size = file_size

    attachment.checksum = checksum

    try:

        db.session.commit()

    except Exception:

        db.session.rollback()

        storage.delete(
    get_attachment_folder(),
    attachment.filename
)

        raise

    try:

        delete_file(
            get_attachment_folder(),
            old_filename
        )

    except Exception as e:

        current_app.logger.error(
            "Unable to delete old attachment '%s'. Error: %s",
            old_filename,
            str(e)
        )

    return attachment


def complete_presigned_upload(
    note_id,
    user_id,
    filename,
    original_filename,
    mime_type,
    file_size
):

    note = Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()

    if not note:

        raise note_exception.NoteNotFoundException(
            "Note not found."
        )

    storage = get_storage()

    exists = storage.exists(
        get_attachment_folder(),
        filename
    )

    if not exists:

        raise BadRequestException(
            "File does not exist in S3."
        )

    attachment = Attachment(

        filename=filename,

        original_filename=
        original_filename,

        file_path=filename,

        mime_type=mime_type,

        file_size=file_size,

        note_id=note.id,

        checksum=""
    )

    db.session.add(
        attachment
    )

    db.session.commit()

    return attachment


def initiate_multipart_upload(
    note_id,
    user_id,
    filename,
    content_type,
    total_parts
):

    note = Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()

    if not note:
        raise note_exception.NoteNotFoundException(
            "Note not found."
        )

    storage = get_storage()

    if current_app.config[
        "UPLOAD_PROVIDER"
    ] != "S3":
        raise BadRequestException(
            "Multipart upload only supported for S3."
        )

    response = storage.initiate_multipart_upload(
            filename=filename,
            folder=get_attachment_folder(),
            content_type=content_type
        )
    

    upload = MultipartUpload(
    upload_id=response["upload_id"],
    filename=response["filename"],
    original_filename=filename,
    note_id=note_id,
    user_id=user_id,
    total_parts=total_parts,
    uploaded_part_numbers=[],
    
    status="INITIATED"
)
    db.session.add(upload)
    db.session.commit()
    response["db_upload_id"] = upload.id

    return response

def get_multipart_part_url(
    user_id,
    attachment_filename,
    upload_id,
    part_number
):

    storage = get_storage()

    if current_app.config[
        "UPLOAD_PROVIDER"
    ] != "S3":

        raise BadRequestException(
            "Multipart upload only supported for S3."
        )

    return (
        storage.get_part_upload_url(
            filename=attachment_filename,
            folder=get_attachment_folder(),
            upload_id=upload_id,
            part_number=part_number
        )
    )

def complete_multipart_attachment(
    note_id,
    user_id,
    filename,
    upload_id,
    parts,
    original_filename,
    content_type,
    file_size
):

    note = Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()

    if not note:
        raise note_exception.NoteNotFoundException(
            "Note not found."
        )

    storage = get_storage()

    response = (
        storage.complete_multipart_upload(
            filename=filename,
            folder=get_attachment_folder(),
            upload_id=upload_id,
            parts=parts
        )
    )
    upload = MultipartUpload.query.filter_by(
    upload_id=upload_id
).first()

    upload.status = "COMPLETED"

    db.session.commit()

    attachment = Attachment(
        filename=filename,
        original_filename=original_filename,
        file_path=filename,
        mime_type=content_type,
        file_size=file_size,
        note_id=note.id,
        checksum=""
    )

    db.session.add(
        attachment
    )

    db.session.commit()

    return attachment

def abort_multipart_attachment(
    user_id,
    filename,
    upload_id
):

    storage = get_storage()

    if current_app.config[
        "UPLOAD_PROVIDER"
    ] != "S3":
        raise BadRequestException(
            "Multipart uploads only supported for S3."
        )

    storage.abort_multipart_upload(
        filename=filename,
        folder=get_attachment_folder(),
        upload_id=upload_id
    )
    upload = MultipartUpload.query.filter_by(
    upload_id=upload_id
).first()
    upload.status = "ABORTED"

    db.session.commit()

    return True

def get_uploaded_parts(
    filename,
    upload_id
):

    storage = get_storage()

    if current_app.config[
        "UPLOAD_PROVIDER"
    ] != "S3":
        raise BadRequestException(
            "Multipart uploads only supported for S3."
        )

    return (
        storage.list_uploaded_parts(
            filename=filename,
            folder=get_attachment_folder(),
            upload_id=upload_id
        )
    )

def mark_part_uploaded(
    upload_id,
    part_number
):

    upload = MultipartUpload.query.filter_by(
        upload_id=upload_id
    ).first()

    if not upload:
        raise BadRequestException(
            "Upload not found."
        )

    current_parts = (
        upload.uploaded_part_numbers
        or []
    )

    if part_number not in current_parts:

        updated_parts = sorted(
            current_parts + [part_number]
        )

        upload.uploaded_part_numbers = (
            updated_parts
        )
        print(
    "Before:",
    current_parts
)

    print(
    "Saving:",
    updated_parts
)

    upload.status = "UPLOADING"

    db.session.commit()
    print(
    "DB:",
    upload.uploaded_part_numbers
)

    db.session.refresh(upload)

    return upload

def get_in_progress_uploads(
    user_id
):  
    return MultipartUpload.query.filter(
    MultipartUpload.user_id == user_id,
    MultipartUpload.status.in_(
        [
            "INITIATED",
            "UPLOADING"
        ]
    )
).all()

def list_uploaded_parts(
    upload_id,
    filename
):

    storage = get_storage()

    return storage.list_parts(
        upload_id=upload_id,
        filename=filename,
        folder=get_attachment_folder()
    )