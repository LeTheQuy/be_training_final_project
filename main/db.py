from flask_sqlalchemy import SQLAlchemy

from main.app import app

db = SQLAlchemy(app)