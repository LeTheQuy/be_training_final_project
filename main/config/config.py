import os
from importlib import import_module

env = os.getenv("ENV", "local")

config_name = "main.config." + env

module = import_module(config_name)

config = module.config

if __name__ == '__main__':
    a = config.get_sqlalchemy_db_uri()
    print(a)
