from main.db import db
from .item import Item


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    password_hash = db.Column(db.String(60), nullable=False)
    items = db.relationship("Item", lazy="dynamic")

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

