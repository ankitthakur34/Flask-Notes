SENSITIVE_FIELDS = {

    "password",

    "token",

    "access_token",

    "refresh_token",

    "authorization",

    "jwt",

    "otp",

    "secret",

    "api_key",

    "reset_token",

    "aws_secret_access_key",

    "mail_password",
    "cloudfront_url"
}


def mask_sensitive_data(
    data
):

    if data is None:
        return None

    if isinstance(
        data,
        dict
    ):

        masked = {}

        for (
            key,
            value
        ) in data.items():

            if (
                key.lower()
                in
                SENSITIVE_FIELDS
            ):

                masked[key] = (
                    "[REDACTED]"
                )

            else:

                masked[key] = (
                    mask_sensitive_data(
                        value
                    )
                )

        return masked

    if isinstance(
        data,
        list
    ):

        return [

            mask_sensitive_data(
                item
            )

            for item in data
        ]

    return data