from datetime import datetime
from app.extensions import db


class ProfileImageVersion(
    db.Model
):

    __tablename__ = (
        "profile_image_versions"
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id"
        ),
        nullable=False
    )

    s3_key = db.Column(
        db.String(255),
        nullable=False
    )

    is_current = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="profile_versions"
    )