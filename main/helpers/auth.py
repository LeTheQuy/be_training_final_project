from functools import wraps

import jwt
from flask import request, jsonify

from main.config.config import config


def encode_identity(identity):
    encoded_jwt = jwt.encode({"identity": identity}, config.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_token(token):
    result = jwt.decode(token, config.SECRET_KEY, algorithms="HS256")
    return result["identity"]


def jwt_required(optional=True):
    def decorator_jwt(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers["Authorization"]
            if not optional:
                if not token or not decode_token(token):
                    return jsonify({"message": "Please authenticate."}), 401
            else:
                pass
            return f(*args, **kwargs)

        return decorated

    return decorator_jwt
