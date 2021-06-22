import functools

import jwt
from flask import request

from main.config.config import config


def encode_identity(identity):
    encoded_jwt = jwt.encode({"identity": identity}, config.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_token(token):
    return jwt.decode(token, config.SECRET_KEY, algorithms="HS256")


def jwt_required(optional=False):
    def decorator_jwt(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            identity = get_jwt_identity()
            if not optional and not identity:
                return {"message": "Unauthorized."}, 401
            kwargs["user_id"] = identity
            return f(*args, **kwargs)

        return decorated

    return decorator_jwt


def get_jwt_identity():
    token = request.headers["Authorization"]
    if not token or not decode_token(token):
        return None
    else:
        return decode_token(token)["identity"]
