from main.db import db


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship("Category")
    user = db.relationship("User")

    def __init__(self, title, description, user_id, category_id):
        self.title = title
        self.description = description
        self.user_id = user_id
        self.category_id = category_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()