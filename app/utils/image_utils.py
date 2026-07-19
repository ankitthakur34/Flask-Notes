from PIL import Image
import io

from app.storage.factory import get_storage
from flask import current_app


THUMBNAIL_SIZES = {
    "small": (50,50),
    "medium": (150,150),
    "large": (300,300)
}

def generate_thumbnails(
    image_file
):

    thumbnails = {}

    image = Image.open(
        image_file
    )

    for (
        name,
        size
    ) in THUMBNAIL_SIZES.items():

        img = image.copy()

        img.thumbnail(size)

        buffer = io.BytesIO()

        img.save(
            buffer,
            format=image.format
        )

        buffer.seek(0)

        thumbnails[name] = buffer

    image_file.seek(0)

    return thumbnails


# def get_profile_urls(
#     profile_key
# ):

#     if not profile_key:
#         return None

#     storage = get_storage()

#     filename = (
#         profile_key.split("/")[-1]
#     )

#     return {

#         "original":
#             storage.get_download_url(
#                 folder="profile",
#                 filename=filename
#             ),

#         "small":
#             storage.get_download_url(
#                 folder=
#                 "profile/thumbs/small",

#                 filename=filename
#             ),

#         "medium":
#             storage.get_download_url(
#                 folder=
#                 "profile/thumbs/medium",

#                 filename=filename
#             ),

#         "large":
#             storage.get_download_url(
#                 folder=
#                 "profile/thumbs/large",

#                 filename=filename
#             )
#     }


def get_cdn_url(
    key
):

    return (
        f"{current_app.config['CLOUDFRONT_URL']}"
        f"/{key}"
    ) 


def get_profile_urls(
    profile_key
):

    if not profile_key:
        return None

    filename = (
        profile_key.split("/")[-1]
    )

    return {

        "original":
            get_cdn_url(
                filename
            ),

        "small":
            get_cdn_url(
                f"thumbs/"
                f"small/"
                f"{filename}"
            ),

        "medium":
            get_cdn_url(
                f"thumbs/"
                f"medium/"
                f"{filename}"
            ),

        "large":
            get_cdn_url(
                f"thumbs/"
                f"large/"
                f"{filename}"
            )
    }