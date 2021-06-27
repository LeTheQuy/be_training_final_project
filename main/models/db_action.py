from main.db import db


class BaseAction:
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_on_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)