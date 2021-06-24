from main.db import db


class DBAction(object):
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_on_db(self):
        db.session.delete(self)
        db.session.commit()
