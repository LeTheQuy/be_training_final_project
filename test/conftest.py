import os
import sys

import pytest

from main.app import app
from main.db import db
from main.helpers.auth import encode_identity
from main.helpers.pw import generate_password_hash
from main.models.category import Category
from main.models.item import Item
from main.models.user import User

if os.getenv('ENV') != 'test':
    print('Tests should be run with "ENV=test"')
    sys.exit(1)

client = app.test_client()


def init_data():
    db.create_all()
    categories = ["FOOTBALL", "TENNIS", "VOLLEYBALL", "SWING", "MARATHON", "JOGGING"]
    root_user = User(username="Quyngao_dz_tqn", password_hash=generate_password_hash("Quy@gotit123"))
    root_user.save_to_db()

    for category in categories:
        c = Category(name=category)
        c.save_to_db()

        for i in range(10):
            item = Item(title=f"{category} Item {i * 1}",
                        description=f"Item description for category {category}, item {i}: A ball is a round object "
                                    f"with various uses. It is used in ball games, where the play of the game follows "
                                    f"the state of the ball as it is hit, kicked or thrown by players.",
                        user_id=root_user.id,
                        category_id=c.id)
            item.save_to_db()


@pytest.fixture(scope="function")
def init_database():
    init_data()
    yield
    db.drop_all()


@pytest.fixture(scope="function")
def login_default_user():
    user = User.find_by_username("Quyngao_dz_tqn")
    return encode_identity(identity=user.id)


if __name__ == '__main__':
    init_data()
