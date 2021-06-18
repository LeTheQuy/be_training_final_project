from flask import request, jsonify
from flask_jwt_extended import create_access_token

from main.app import app
from main.helpers.pw import generate_password_hash, verify_password_with_password_hash
from main.models.user import User


@app.route("/auth/signup", methods=["POST"])
def register_user():
    request_data = request.get_json()
    if User.find_by_username(request_data["username"]):
        return jsonify({"message": "Duplicated username"}), 400
    else:
        password_hash = generate_password_hash(request_data["password"])
        user = User(username=request_data["username"], password_hash=password_hash)
        user.save_to_db()
        return jsonify({"message": "User created successfully"}), 201


@app.route("/auth/sign_in", methods=["POST"])
def sign_in():
    request_data = request.get_json()
    user = User.find_by_username(request_data["username"])
    if user and verify_password_with_password_hash(request_data["password"], user.password_hash):
        access_token = create_access_token(identity=user.id, fresh=True)
        return {"access_token": access_token}, 200
    else:
        return {"message": "User not found"}, 401
