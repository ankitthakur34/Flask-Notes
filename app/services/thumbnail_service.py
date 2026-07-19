from app.storage import (
    get_storage
)

from app.utils.image_utils import (
    generate_thumbnails
)

def create_profile_thumbnails(
    key,
    content_type="image/jpeg"
):

    storage = get_storage()

    image = (
        storage.get_file_object(
            key
        )
    )

    thumbnails = (
        generate_thumbnails(
            image
        )
    )

    filename = key.split("/")[-1]

    for (
        size,
        file_obj
    ) in thumbnails.items():

        thumbnail_key = (
            f"profile/thumbs/"
            f"{size}/"
            f"{filename}"
        )

        storage.upload_file_object(
            file_obj,
            thumbnail_key,
            content_type
        )