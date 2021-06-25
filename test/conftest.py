import os

import pytest

from main.app import app
from main.db import db
from main.models.category import Category

os.environ["ENV"] = "test"

client = app.test_client()


def init_data():
    db.create_all()
    categories = ["FOOTBALL", "TENNIS", "VOLLEYBALL", "SWING", "MARATHON", "JOGGING"]
    for category in categories:
        c = Category(name=category)
        c.save_to_db()


@pytest.fixture(scope='function')
def init_database():
    init_data()
    yield
    db.drop_all()


if __name__ == '__main__':
    init_data()
