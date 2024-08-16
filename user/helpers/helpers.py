import jwt
import time
import uuid
import json
import hashlib
from typing import Tuple
from Config import config
from pytz import country_timezones
from django.http import HttpResponse
from itsdangerous import TimestampSigner


def generate_jwt_token(user_id):
    token_metadata = {
        "uid": user_id,
        "iat": int(time.time()),
        "exp": int(time.time()) + config.token_expiry,
    }

    jwt_token = jwt.encode(token_metadata, key=config.jwt_secret)
    return TimestampSigner(config.jwt_secret).sign(jwt_token).decode("utf-8")

def validate_gql_access_token(func) -> Tuple[bool, uuid.UUID]:
    def validator(self, root, info, **kwargs) -> Tuple[bool, uuid.UUID]:
        if not info.context.headers.get("Authorization"):
            return bad_request(
                operation="",
                model="",
                message="Not Authorized",
                message_key="not-authorized",
            )

        access_token = info.context.headers["Authorization"].split()[-1]
        signer = TimestampSigner(config.jwt_secret)
        if not signer.validate(access_token):
            return bad_request(
                operation="",
                model="",
                message="Token Expired",
                message_key="token-expired",
            )

        jwt_meta = jwt.decode(
            signer.unsign(access_token, max_age=config.token_expiry).decode("utf-8"),
            key=config.jwt_secret,
            algorithms="HS256",
        )

        return func(self, info, user_id=jwt_meta["uid"], **kwargs)

    return validator

def validate_access_token(func) -> Tuple[bool, uuid.UUID]:
    def validator(request, **kwargs) -> Tuple[bool, uuid.UUID]:
        if not request.headers.get("Authorization"):
            return HttpResponse(
                "Not Authorized",
                content_type="text/plain",
                status=401,
            )

        access_token = request.headers["Authorization"].split()[-1]
        signer = TimestampSigner(config.jwt_secret)
        if not signer.validate(access_token):
            return HttpResponse(
                "Token Expired",
                content_type="text/plain",
                status=401,
            )

        jwt_meta = jwt.decode(
            signer.unsign(access_token, max_age=config.token_expiry).decode("utf-8"),
            key=config.jwt_secret,
            algorithms="HS256",
        )

        request.META["PROFILE"] = jwt_meta["uid"]
        return func(request, **kwargs)

    return validator


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (uuid.UUID)):
            return str(obj)
        return super().default(obj)


def encode_password(password: str) -> str:
    return hashlib.sha256((password or "").strip().encode("UTF-8")).hexdigest()


def json_response(data: dict):
    return json.dumps(data, cls=JSONEncoder)
