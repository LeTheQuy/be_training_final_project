from flask import Flask, jsonify

from main.config.config import config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{config.MYSQL_USERNAME}:{config.MYSQL_PASSWORD}" \
                                        f"@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DB}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = config.SECRET_KEY


@app.errorhandler(404)
def resource_not_found(e):
    return {"message": str(e)}, 404


@app.errorhandler(500)
def internal_server_error(e):
    return {"message": str(e)}, 500


@app.errorhandler(401)
def unauthorized(e):
    return {"message": "Unauthorized", }, 401


@app.errorhandler(403)
def forbidden(e):
    return {"message": "Forbidden, permission denied"}, 403


def _register_modules():
    import main.models
    import main.controllers


_register_modules()
