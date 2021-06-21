from sqlalchemy import asc

from main.db import db


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=True)
    items = db.relationship("Item", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.order_by(asc(cls.name))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
