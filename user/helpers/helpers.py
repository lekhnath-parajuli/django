import jwt
import time
import uuid
import json
import hashlib
from Config import config
from itsdangerous import TimestampSigner


def generate_jwt_token(user_id):
    token_metadata = {
        "uid": user_id,
        "iat": int(time.time()),
        "exp": int(time.time()) + config.token_expiry,
    }

    jwt_token = jwt.encode(token_metadata, key=config.jwt_secret)
    return TimestampSigner(config.jwt_secret).sign(jwt_token).decode("utf-8")


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (uuid.UUID)):
            return str(obj)
        return super().default(obj)


def encode_password(password: str) -> str:
    return hashlib.sha256(password).hexdigest()


def json_response(data: dict):
    return json.dumps(data, cls=JSONEncoder)
