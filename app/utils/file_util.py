import os
import uuid
import hashlib

from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename


from werkzeug.utils import secure_filename

def generate_unique_filename(filename):

    filename = secure_filename(filename)

    extension = os.path.splitext(filename)[1].lower()

    return f"{uuid.uuid4()}{extension}"

def save_file(file, upload_folder):

    filename = generate_unique_filename(
        file.filename
    )
    

    path = os.path.join(
        upload_folder,
        filename
    )

    file.save(path)

    return filename

def delete_file(
    upload_folder,
    filename
):

    if not filename:
        return

    path = os.path.join(
        upload_folder,
        filename
    )

    if os.path.exists(path):

        os.remove(path)

def allowed_extension(
    filename,
    allowed_extensions
):

    if "." not in filename:

        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in allowed_extensions

def verify_image(file):

    try:

        img = Image.open(file)

        img.verify()

        file.seek(0)

        return True

    except Exception:

        return False
    
def get_file_size(file):

    file.seek(0, os.SEEK_END)

    size = file.tell()

    file.seek(0)

    return size

def allowed_mime_type(file, allowed_mime_types):

    return file.content_type in allowed_mime_types  


from flask import current_app

from app.exceptions import BadRequestException


def validate_uploaded_file(
    file,
    allowed_extensions,
    allowed_mime_types,
    verify_image_file=False,
    max_size=None
):
    """
    Generic validation for uploaded files.
    """

    if not file:
        raise BadRequestException(
            "File is required."
        )

    if file.filename == "":
        raise BadRequestException(
            "Invalid filename."
        )

    # Extension validation
    if not allowed_extension(
        file.filename,
        allowed_extensions
    ):
        raise BadRequestException(
            "Invalid file extension."
        )

    # MIME validation
    if not allowed_mime_type(
        file,
        allowed_mime_types
    ):
        raise BadRequestException(
            "Invalid MIME type."
        )

    # File size validation
    file_size = get_file_size(file)

    if max_size and file_size > max_size:

        raise BadRequestException(
            f"Maximum allowed file size is {max_size // (1024 * 1024)} MB."
        )

    # Verify image only when required
    if (
        verify_image_file
        and file.content_type.startswith("image/")
    ):

        if not verify_image(file):

            raise BadRequestException(
                "Invalid image."
            )

    return file_size


def calculate_checksum(file):

    sha256 = hashlib.sha256()

    current_position = file.stream.tell()

    file.stream.seek(0)

    while True:

        chunk = file.stream.read(8192)

        if not chunk:

            break

        sha256.update(chunk)

    checksum = sha256.hexdigest()

    file.stream.seek(current_position)

    return checksum







  



  



