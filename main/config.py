import os
from importlib import import_module

env = os.getenv("ENV", "local")

config_name = "config." + env

module = import_module(config_name)

config = module.config
