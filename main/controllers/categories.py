from main.app import app
from main.helpers.parser import parse_category
from main.models.category import Category
from main.schemas.base.category import CategorySchema


@app.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.find_all()
    result = CategorySchema(many=True, only=("id", "name")).dump(categories)
    return result


@app.route("/categories/<int:category_id>", methods=["GET"])
@parse_category()
def get_category_by_id(category_id, category):
    data = CategorySchema().dump(category)
    return data
