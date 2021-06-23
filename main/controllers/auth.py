from flask import abort

from main.app import app
from main.helpers.auth import encode_identity
from main.helpers.pw import generate_password_hash, verify_password_with_password_hash
from main.models.user import User
from main.schemas.base.user import UserSchema
from main.schemas.user_signup import UserSignUpSchema
from main.schemas.validation import load_request_data_by_schema

user_schema = UserSchema(exclude=("items",))


@app.route("/auth/sign-up", methods=["POST"])
@load_request_data_by_schema(UserSignUpSchema())
def register_user(request_data):
    if User.find_by_username(request_data["username"]):
        return {"message": "Duplicated username"}, 400
    else:
        password_hash = generate_password_hash(request_data["password"])
        user = User(username=request_data["username"], password_hash=password_hash)
        user.save_to_db()
        data = UserSignUpSchema(exclude=("items",)).dump(user)
        return {"user": data, "message": "User created successfully"}, 201


@app.route("/auth/sign-in", methods=["POST"])
@load_request_data_by_schema(UserSchema())
def sign_in(request_data):
    user = User.find_by_username(request_data["username"])
    if user and verify_password_with_password_hash(request_data["password"], user.password_hash):
        access_token = encode_identity(identity=user.id)
        return {"access_token": access_token}, 200
    abort(401)
