from sqlalchemy import desc

from main.db import db
from main.models.db_action import BaseAction


class Item(db.Model, BaseAction):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45), nullable=False, unique=True)
    description = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    category = db.relationship("Category")
    user = db.relationship("User")

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).one_or_none()

    @classmethod
    def find_all(cls, limit=None):
        if limit:
            return cls.query.limit(limit).all()
        else:
            return cls.query.all()

    @classmethod
    def get_latest_added_list(cls, limit):
        return cls.query.order_by(desc(cls.id)).limit(limit)

    @classmethod
    def get_items_per_page(cls, category_id, page, per_page):
        return cls.query.filter_by(category_id=category_id).paginate(page, per_page, error_out=True)
