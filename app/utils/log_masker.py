SENSITIVE_FIELDS = {

    "password",

    "token",

    "access_token",

    "refresh_token",

    "secret",

    "otp",

    "authorization",

    "api_key",

    "jwt"
}

def mask_data(
    data
):

    if not isinstance(
        data,
        dict
    ):
        return data

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
                "******"
            )

        else:

            masked[key] = value

    return masked