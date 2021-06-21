from flask import jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from main.app import app
from main.models.category import Category
from main.models.schemas import categories_schema, category_schema


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
        data = {"message": "invalid category id"}
    return jsonify(data)


@app.route("/categories/<string:name>", methods=["POST"])
@jwt_required()
def add_category(name):
    try:
        category_schema.load({"name": name})
    except ValidationError as err:
        return jsonify({"message": err.messages})

    category = Category.find_by_name(name)
    if category:
        return jsonify({"message": "Duplicated category name"}), 400
    else:
        category = Category(name)
        category.save_to_db()
        result = category_schema.dump(category)
        result["message"] = "Category added"
        return jsonify(result)
