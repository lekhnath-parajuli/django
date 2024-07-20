import uuid
import json
import hashlib


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (uuid.UUID)):
            return str(obj)
        return super().default(obj)


def encode_password(password: str) -> str:
    return hashlib.sha256(password).hexdigest()


def json_response(data: object):
    return json.dumps(data.__dict__, cls=JSONEncoder)
