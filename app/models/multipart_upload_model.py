# from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList

from datetime import datetime

from app.extensions import db


class MultipartUpload(db.Model):

    __tablename__ = "multipart_uploads"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    upload_id = db.Column(
        db.String(255),
        nullable=False,
        unique=True
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    original_filename = db.Column(
        db.String(255),
        nullable=False
    )

    note_id = db.Column(
        db.Integer,
        db.ForeignKey("notes.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    total_parts = db.Column(
        db.Integer,
        nullable=False
    )

    # uploaded_part_numbers = db.Column(
    #     ARRAY(db.Integer),
    #     default=0
    # )
    uploaded_part_numbers = db.Column(
    MutableList.as_mutable(db.JSON),
    default=list
)

    status = db.Column(
        db.String(50),
        default="INITIATED"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )