from sqlalchemy import desc

from main.db import db


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45), nullable=False, unique=True)
    description = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    category = db.relationship("Category")
    user = db.relationship("User")

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_on_db(self):
        db.session.delete(self)
        db.session.commit()
