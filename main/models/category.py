from main.db import db
from main.models.db_action import BaseAction


class Category(db.Model, BaseAction):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=True)

    items = db.relationship("Item", lazy="dynamic")

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).one_or_none()

    @classmethod
    def find_all(cls):
        return cls.query.all()
