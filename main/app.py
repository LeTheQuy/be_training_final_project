from flask import Flask

from main.config.config import config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.get_sqlalchemy_db_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = config.SECRET_KEY


@app.route("/")
def hello():
    return {"hello": "world"}


def _register_modules():
    import main.models
    import main.controllers


_register_modules()
