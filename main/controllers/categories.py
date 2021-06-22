from main.app import app
from main.helpers.auth import jwt_required
from main.models.category import Category
from main.schemas.category_schema import CategorySchema
from main.schemas.validation import load_request_data_by_schema

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True, only=("id", "name"))


@app.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.find_all()
    result = categories_schema.dump(categories)
    return result


@app.route("/categories/<int:_id>", methods=["GET"])
def get_category_by_id(_id):
    category = Category.find_by_id(_id)
    if category:
        data = category_schema.dump(category)
    else:
        data = {"message": "invalid category id"}, 400
    return data


@app.route("/categories/<string:name>", methods=["POST"])
@jwt_required()
def add_category(name, user_id):
    category = Category.find_by_name(name)
    if category:
        return {"message": "Duplicated category name"}, 400
    else:
        category = Category(name=name)
        category.save_to_db()
        result = category_schema.dump(category)
        result["message"] = "Category added"
        return result
