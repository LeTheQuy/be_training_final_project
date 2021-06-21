from main.db import db
from main.helpers.pw import generate_password_hash
from main.models.category import Category
from main.models.item import Item
from main.models.user import User

db.drop_all()
db.create_all()

root_user = User("root", generate_password_hash("123456"))
root_user.save_to_db()

CATEGORIES = ["FOOTBALL", "TENNIS", "VOLLEYBALL", "SWING", "MARATHON", "JOGGING"]

for category in CATEGORIES:
    Category(category).save_to_db()
    for i in range(10):
        item = Item(f"{category} Item {i*1}", f"Item description for category {category}, item {i}: A ball is a round object with "
                                 f"various uses. It is used in ball games, where the play of the game follows the "
                                 f"state of the ball as it is hit, kicked or thrown by players. ",
                    root_user.id, Category.find_all()[0].id)
        item.save_to_db()
