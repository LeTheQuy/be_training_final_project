from flask import request
from marshmallow import ValidationError

from main.app import app
from main.config.config import config
from main.helpers.auth import jwt_required, get_jwt_identity
from main.models.category import Category
from main.models.item import Item
from main.models.schemas import item_schema, items_schema


@app.route("/items", methods=["GET"])
def get_latest_added_items():
    order = request.args.get("order")
    if order:
        items_per_page = request.args.get("items_per_page", config.ITEM_PER_PAGE)
        try:
            items_per_page = int(items_per_page)
        except:
            return {"message": "Invalid items_per_page param"}, 400
        if order != "newest":
            return {"message": "Invalid limit param"}, 400
        items = Item.get_latest_added_list(limit=items_per_page)
    else:
        items = Item.find_all()
    result = items_schema.dump(items)
    return result


@app.route("/categories/<int:category_id>/items")
def get_items_by_category_id(category_id):
    try:
        page = int(request.args.get("page", 1))
        items_per_page = int(request.args.get("items_per_page", config.ITEM_PER_PAGE))
    except:
        return {"message": "Invalid params"}

    category = Category.find_by_id(category_id)
    if category is None:
        return {"message": "Invalid category id"}, 400

    pagination = Item.get_items_per_page(page, items_per_page)
    items = pagination.items

    result = items_schema.dump(items)
    result["current_page"] = page
    result["total_items"] = pagination.total
    result["items_per_page"] = len(items)
    return result


@app.route("/categories/<int:category_id>/items/<int:item_id>")
@jwt_required(optional=True)
def get_item_detail(category_id, item_id):
    user_id = get_jwt_identity()

    category = Category.find_by_id(category_id)
    if category is None:
        return {"message": "Invalid category id"}, 400

    item = Item.find_by_id(item_id)
    if item is None:
        return {"message": "Invalid item id"}, 400

    if item.category.id != category_id:
        return {"message": "Category and item don't match"}, 400

    result = item_schema.dump(item)

    result["editable"] = True if user_id else False

    return result


@app.route("/categories/<int:category_id>/items", methods=["POST"])
@jwt_required()
def add_item(category_id):
    try:
        request_data = item_schema.load(request.get_json())
    except ValidationError as err:
        return {"message": err.messages}, 400
    user_id = get_jwt_identity()
    category = Category.find_by_id(category_id)
    if category is None:
        return {"message": "Invalid category id"}, 400

    if Item.find_by_name(request_data["title"]):
        return {"message": "Duplicated item title"}, 400

    item = Item(request_data["title"], request_data["description"], user_id, category_id)
    item.save_to_db()
    result = item_schema.dump(item)
    return {
               "message": "Item added", "item": result
           }, 201


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_item_info(category_id, item_id):
    try:
        request_data = item_schema.load(request.get_json())
    except ValidationError as err:
        return {"message": err.messages}, 400

    category = Category.find_by_id(category_id)
    if category is None:
        return {"message": "Invalid category id"}, 400

    item = Item.find_by_id(item_id)
    if item is None:
        return {"message": "Invalid item id"}, 400

    if item.category.id != category_id:
        return {"message": "Category and item don't match"}, 400

    item.title = request_data["title"]
    item.description = request_data["description"]
    item.category_id = request_data["category_id"]
    item.save_to_db()
    result = item_schema.dump(item)
    return {"message": "Item updated", "item": result}


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_item_info(category_id, item_id):
    category = Category.find_by_id(category_id)
    if category is None:
        return {"message": "Invalid category id"}, 400

    item = Item.find_by_id(item_id)
    if item is None:
        return {"message": "Invalid item id"}, 400

    if item.category.id != category_id:
        return {"message": "Category and item don't match"}, 400

    item.delete_on_db()
    result = item_schema.dump(item)
    return {"message": "Item deleted", "item": result}
