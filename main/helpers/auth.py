import functools

import jwt
from flask import request, abort

from main.config.config import config
from main.models.user import User


def encode_identity(identity):
    try:
        encoded_jwt = jwt.encode({"identity": identity}, config.SECRET_KEY, algorithm="HS256")
        return encoded_jwt
    except Exception as e:
        abort(400, description=str(e))


def decode_token(token):
    try:
        return jwt.decode(token, config.SECRET_KEY, algorithms="HS256")
    except Exception as e:
        abort(401, description=str(e))


def _get_jwt_identity():
    if "Authorization" not in request.headers or not request.headers["Authorization"]:
        return None
    token = request.headers["Authorization"]
    decoded_jwt = decode_token(token)

    if not decoded_jwt or not decoded_jwt["identity"]:
        return None
    return decoded_jwt["identity"]


def jwt_required(required=True):
    def decorator_jwt(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            identity = _get_jwt_identity()
            if required and not identity or not User.find_by_id(identity):
                abort(401)
            # Auto add user_id as kwargs for a method
            kwargs["user_id"] = identity
            return f(*args, **kwargs)

        return decorated

    return decorator_jwt
