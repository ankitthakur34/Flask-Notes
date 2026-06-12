import json
from app.extensions import redis_client
from app.logging_config import logger

def get_cached_note(user_id, note_id):

    key = f"note:{user_id}:{note_id}"

    data = redis_client.get(key)

    if data:
        logger.info(f"Cache hit for key: {key}")
        return json.loads(data)
    logger.info(f"Cache miss for key: {key}")
    return None


def set_cached_note(user_id, note_id, note_data):

    key = f"note:{user_id}:{note_id}"
    logger.info(f"Setting cache for key: {key} with data: {note_data}")
    redis_client.setex(
        key,
        300,
        json.dumps(note_data)
    )


def delete_cached_note(user_id, note_id):

    key = f"note:{user_id}:{note_id}"
    logger.info(f"Deleting cache for key: {key}")
    redis_client.delete(key)