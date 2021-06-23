from main.config.base import BaseConfig


class LocalConfig(BaseConfig):
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_USERNAME = "root"
    MYSQL_PASSWORD = "quyngao123456"
    MYSQL_DB = "be_training"
    DEBUG = True
    SECRET_KEY = "be_training_g0tit@^&#quydz__tqn_"
    ITEMS_PER_PAGE = 10


config = LocalConfig
