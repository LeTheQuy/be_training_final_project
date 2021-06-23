from main.db import db
from .item import Item


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    password_hash = db.Column(db.String(60), nullable=False)

    items = db.relationship("Item", lazy="dynamic")

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
