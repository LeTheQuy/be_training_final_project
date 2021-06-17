from main.config.base import _Config


class _LocalConfig(_Config):
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_USERNAME = "root"
    MYSQL_PASSWORD = "quyngao123456"
    MYSQL_DB = "be_training"
    DEBUG = True
    SECRET_KEY = "quydzzzz"


config = _LocalConfig
