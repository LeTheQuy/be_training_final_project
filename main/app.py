from flask import Flask
from flask_jwt_extended import JWTManager

from main.config.local import config
from main.db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.get_sqlalchemy_db_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = config.SECRET_KEY
app.config["JWT_SECRET_KEY"] = config.SECRET_KEY

jwt = JWTManager(app)


@app.route('/')
def hello():
    return {"hello": "world"}


def _register_modules():
    import main.models
    import main.controllers


_register_modules()


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
