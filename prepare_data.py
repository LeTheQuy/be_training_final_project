from main.db import db
from main.helpers.pw import generate_password_hash
from main.models.category import Category
from main.models.item import Item
from main.models.user import User

db.drop_all()
db.create_all()

root_user = User("root", generate_password_hash("123456"))
root_user.save_to_db()

CATEGORIES = ["FOODBALL", "TENNIS", "VOLLEYBALL", "SWING", "MARATHON", "JOGGING"]

for category in CATEGORIES:
    Category(category).save_to_db()

item = Item("First Item", "Fist Item description ..... ", root_user.id, Category.find_all()[0].id)
item.save_to_db()
