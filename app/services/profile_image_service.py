from app.extensions import db
from app.repositories.user_repositories import get_user_by_id


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

    storage = get_storage()

    if user.profile_image:

        old_key = (
            user.profile_image
        )

        filename = (
            old_key.replace(
                "profile/",
                ""
            )
        )

        storage.delete(
            get_profile_folder(),
            filename
        )

    user.profile_image = key

    db.session.commit()

    return user