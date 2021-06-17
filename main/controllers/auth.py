from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token

from main.app import app
from main.models.user import User


@app.route("/auth/signup", methods=["POST"])
def register_user():
    request_data = request.get_json()
    if User.find_by_username(request_data["username"]):
        return jsonify({"message": "Duplicated username"}), 400
    else:
        user = User(**request_data)
        user.save_to_db()
        return jsonify({"message": "User created successfully"}), 201


@app.route("/auth/sign_in", methods=["POST"])
def sign_in():
    request_data = request.get_json()
    user = User.find_by_username(request_data["username"])
    if user and user.password == request_data["password"]:
        access_token = create_access_token(identity=user.id, fresh=True)
        return {"access_token": access_token}, 200
    else:
        return {"message": "User not found"}, 401
