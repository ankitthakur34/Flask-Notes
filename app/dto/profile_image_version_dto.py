class ProfileImageVersionDTO:

    @staticmethod
    def to_response(
        version
    ):
        return {
            "id":
                version.id,

            "key":
                version.s3_key,

            "is_current":
                version.is_current,

            "created_at":
                version.created_at
        }