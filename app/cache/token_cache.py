from app.extensions import redis_client
from app.logging_config import logger

def blacklist_token(jti,expires_in):
    logger.info("setting token in blacklist redis")
    redis_client.setex(
         f"blacklist:{jti}",
        expires_in,
        "true"
    )

def is_token_blacklisted(jti):
    logger.info("checking is token is blacklisted or not")
    return redis_client.exists(
        f"blacklist:{jti}"
    )    