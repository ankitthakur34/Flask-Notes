from .db import db
from .migrate import migrate
from .jwt import jwt
from .redis import redis_client
from .blacklist_token import check_if_token_revoked
from .flask_mail import mail