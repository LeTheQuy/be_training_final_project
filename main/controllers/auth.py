from flask import request, jsonify
from marshmallow import ValidationError

from main.app import app
from main.helpers.auth import encode_identity
from main.helpers.pw import generate_password_hash, verify_password_with_password_hash
from main.models.schemas import user_schema
from main.models.user import User


@app.route("/auth/signup", methods=["POST"])
def register_user():
    try:
        request_data = user_schema.load(request.get_json())
    except ValidationError as err:
        return {"message": err.messages}, 400

    if User.find_by_username(request_data["username"]):
        return jsonify({"message": "Duplicated username"}), 400
    else:
        password_hash = generate_password_hash(request_data["password"])
        user = User(username=request_data["username"], password_hash=password_hash)
        user.save_to_db()
        data = user_schema.dump(user)
        data["message"] = "User created successfully"
        return data, 201


@app.route("/auth/sign_in", methods=["POST"])
def sign_in():
    try:
        request_data = user_schema.load(request.get_json())
    except ValidationError as err:
        return {"message": err.messages}, 400

    user = User.find_by_username(request_data["username"])
    if user:
        if verify_password_with_password_hash(request_data["password"], user.password_hash):
            access_token = encode_identity(identity=user.id)
            return {"access_token": access_token}, 200
        else:
            return {"message": "Incorrect Password"}, 401
    else:
        return {"message": "User not found"}, 401
