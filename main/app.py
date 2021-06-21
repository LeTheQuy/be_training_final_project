from flask import Flask

from main.config.config import config

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{config.MYSQL_USERNAME}:{config.MYSQL_PASSWORD}" \
                                 f"@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DB}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = config.SECRET_KEY


def _register_modules():
    import main.models
    import main.controllers


_register_modules()
