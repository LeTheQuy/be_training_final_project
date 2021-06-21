from flask import jsonify

from main.app import app
from main.helpers.auth import encode_identity
from main.helpers.pw import generate_password_hash, verify_password_with_password_hash
from main.models.user import User
from main.schemas.user_shema import UserSchema
from main.schemas.validation import load_request_data_by_schema

user_schema = UserSchema(exclude=("items",))


@app.route("/auth/sign_up", methods=["POST"])
@load_request_data_by_schema(user_schema)
def register_user(request_data):
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
@load_request_data_by_schema(user_schema)
def sign_in(request_data):
    user = User.find_by_username(request_data["username"])
    if user:
        if verify_password_with_password_hash(request_data["password"], user.password_hash):
            access_token = encode_identity(identity=user.id)
            return {"access_token": access_token}, 200
    return {"message": "Unauthorized"}, 401
