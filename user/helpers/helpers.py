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


def get_timezone_country_code_map():
    timezone_to_country_code_map = {}
    for country_code in country_timezones:
        for timezone in country_timezones[country_code]:
            timezone_to_country_code_map[timezone] = country_code
    timezone_to_country_code_map["GMT"] = "US"
    return timezone_to_country_code_map


def convert_to_E164_format(phone):
    if not phone:
        return phone
    return phonenumbers.format_number(
        phonenumbers.parse(phone, code),
        phonenumbers.PhoneNumberFormat.E164,
    )
