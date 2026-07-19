from app.extensions import db
from app.repositories.user_repositories import get_user_by_id
from app.models import (
    ProfileImageVersion
)


from app.services.thumbnail_service import create_profile_thumbnails
from app.storage.factory import get_profile_folder,get_storage

def generate_profile_upload_url(
    user_id,
    filename,
    content_type
):
    storage = get_storage()

    response = (
        storage.get_upload_url(
            filename=filename,
            folder=get_profile_folder(),
            content_type=content_type
        )
    )

    return response

def confirm_profile_upload(
    user_id,
    key
):

    user = get_user_by_id(
        user_id
    )

    old_version = (
        ProfileImageVersion
        .query
        .filter_by(
            user_id=user.id,
            is_current=True
        )
        .first()
    )

    if old_version:

        old_version.is_current = (
            False
        )

    version = (
        ProfileImageVersion(
            user_id=user.id,
            s3_key=key,
            is_current=True
        )
    )

    db.session.add(
        version
    )

    user.profile_image = key

    db.session.commit()
    create_profile_thumbnails(
    key
)

    return user

def get_profile_versions(
    user_id
):

    return (
        ProfileImageVersion
        .query
        .filter_by(
            user_id=user_id
        )
        .order_by(
            ProfileImageVersion
            .created_at.desc()
        )
        .all()
    )