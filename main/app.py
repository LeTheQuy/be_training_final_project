from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from main.config.local import config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.get_sqlalchemy_db_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = config.SECRET_KEY
app.config["JWT_SECRET_KEY"] = config.SECRET_KEY

jwt = JWTManager(app)
bcrypt = Bcrypt(app)


@app.route("/")
def hello():
    return {"hello": "world"}


def _register_modules():
    import main.models
    import main.controllers


_register_modules()
