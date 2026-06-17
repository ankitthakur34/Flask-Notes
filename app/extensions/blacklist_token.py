from app.cache.token_cache import is_token_blacklisted

def check_if_token_revoked(
    jwt_header,
    jwt_payload
):

    jti = jwt_payload["jti"]

    return is_token_blacklisted(jti)