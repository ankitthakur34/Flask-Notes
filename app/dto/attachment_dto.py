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
    
    def multipart_to_response(
    upload
):

        return {
        "id":
            upload.id,

        "upload_id":
            upload.upload_id,

        "filename":
            upload.filename,

        "original_filename":
            upload.original_filename,

        "note_id":
            upload.note_id,

        "status":
            upload.status,

        "total_parts":
            upload.total_parts,

        "uploaded_parts":
            upload.uploaded_part_numbers
    }