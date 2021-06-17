from flask import jsonify
from flask_jwt_extended import jwt_required

from main.app import app
from main.models.category import Category


@app.route("/categories", methods=["GET"])
def get_categories():
    return jsonify({
        [category.json() for category in Category.find_all()]
    })


@app.route("/categories/<int:_id>", methods=["GET"])
def get_category_by_id(_id):
    category = Category.find_by_id(_id)
    data = category.json()
    data["items"] = [{"id": item.id, "title": item.title} for item in category.items.all()]
    return jsonify(data)


@jwt_required()
@app.route("/categories/<string:name>", methods=["POST"])
def add_category(name):
    category = Category.find_by_name(name)
    if category:
        return jsonify({"message": "Duplicated category name"}), 400
    else:
        category = Category(name)
        category.save_to_db()
        return jsonify({"message": "Item added "})
