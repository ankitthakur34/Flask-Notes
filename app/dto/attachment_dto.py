from app.models import Attachment


class AttachmentDTO:

    @staticmethod
    def to_response(
        attachment: Attachment
    ):

        return {
            "id": attachment.id,
            "filename": attachment.original_filename,
            "mime_type": attachment.mime_type,
            "size": attachment.file_size,
            "created_at": attachment.created_at,
            "download_url": f"/attachments/{attachment.id}/download"
        }

    @staticmethod
    def to_list(
        attachments
    ):

        return [
            AttachmentDTO.to_response(a)
            for a in attachments
        ]