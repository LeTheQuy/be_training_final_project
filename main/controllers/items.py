from marshmallow import ValidationError

from main.app import app
from main.helpers.auth import jwt_required
from main.models.category import Category
from main.models.item import Item
from main.schemas.item_schema import ItemSchema
from main.schemas.category_item_schema import get_item_by_condition
from main.schemas.pagination_schema import PaginationSchema
from main.schemas.order_item_schema import OrderItemSchema
from main.schemas.validation import load_request_data_by_schema

item_schema = ItemSchema(only=("id", "title", "description", "category_id", "category.id", "category.name"))

items_schema = ItemSchema(many=True, only=("id", "title", "description", "category.id", "category.name"))


@app.route("/items", methods=["GET"])
@load_request_data_by_schema(OrderItemSchema())
def get_latest_added_items(request_data):
    items = request_data
    result = items_schema.dump(items)
    return result


@app.route("/categories/<int:category_id>/items")
@load_request_data_by_schema(PaginationSchema())
def get_items_by_category_id(category_id, request_data):
    category = Category.find_by_id(category_id)
    if category is None:
        return {"message": "Invalid category id"}, 400

    pagination = Item.get_items_per_page(category_id=category_id,
                                         page=request_data["page"],
                                         per_page=request_data["items_per_page"])
    items = pagination.items

    result = items_schema.dump(items)
    result["current_page"] = request_data["page"]
    result["total_items"] = pagination.total
    result["items_per_page"] = len(items)
    return result


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["GET"])
@jwt_required(optional=False)
def get_item_detail(category_id, item_id, user_id):
    try:
        item = get_item_by_condition(category_id=category_id, item_id=item_id, user_id=user_id)
    except ValidationError as err:
        return {"message": err.messages}, 400
    result = item_schema.dump(item)
    result["editable"] = False if not user_id else True
    return result


@app.route("/categories/<int:category_id>/items", methods=["POST"])
@jwt_required()
@load_request_data_by_schema(item_schema)
def add_item(category_id, user_id, request_data):
    category = Category.find_by_id(category_id)
    if category is None:
        return {"message": "Invalid category id"}, 400

    if Item.find_by_title(request_data["title"]):
        return {"message": "Duplicated item title"}, 400

    item = Item(title=request_data["title"],
                description=request_data["description"],
                user_id=user_id,
                category_id=category_id)
    item.save_to_db()
    result = item_schema.dump(item)
    result["message"] = "Item added"

    return result, 201


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["PUT"])
@jwt_required()
@load_request_data_by_schema(item_schema)
def update_item_info(category_id, item_id, user_id, request_data):
    try:
        item = get_item_by_condition(category_id=category_id, item_id=item_id, user_id=user_id)
    except ValidationError as err:
        return {"message": err.messages}, 400
    item.title = request_data["title"]
    item.description = request_data["description"]
    item.category_id = request_data["category_id"]
    item.save_to_db()
    result = item_schema.dump(item)
    result["message"] = "Item updated"
    return result


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_item_info(category_id, item_id, user_id):
    try:
        item = get_item_by_condition(category_id=category_id, item_id=item_id, user_id=user_id)
    except ValidationError as err:
        return {"message": err.messages}, 400
    item.delete_on_db()
    result = item_schema.dump(item)
    result["message"] = "Item deleted"
    return result
