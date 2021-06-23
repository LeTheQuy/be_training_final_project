from main.app import app
from main.helpers.auth import jwt_required
from main.helpers.parser import parse_data
from main.models.category import Category
from main.models.item import Item
from main.schemas.base.item import ItemSchema, dump_simple_item
from main.schemas.pagination_schema import PaginationSchema
from main.helpers.schema import load_request_data_by_schema


@app.route("/items", methods=["GET"])
@load_request_data_by_schema(PaginationSchema())
def get_latest_added_items(request_data):
    if "order" in request_data:
        items = Item.get_latest_added_list(request_data["items_per_page"])
    else:
        items = Item.find_all(request_data["items_per_page"])

    result = dump_simple_item(items, many=True)
    return result


@app.route("/categories/<int:category_id>/items", methods=["GET"])
@parse_data()
@load_request_data_by_schema(PaginationSchema())
def get_items_by_category_id(category_id, request_data, category):
    pagination = category.items.paginate(page=request_data["page"], per_page=request_data["items_per_page"],
                                         error_out=True)
    items = pagination.items

    result = dump_simple_item(items, many=True)
    result["current_page"] = request_data["page"]
    result["total_items"] = pagination.total
    result["items_per_page"] = request_data["items_per_page"]
    return result


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["GET"])
@jwt_required(required=False)
@parse_data(check_editable=False)
def get_item_detail(category_id, item_id, user_id, category, item):
    result = dump_simple_item(item)
    result["editable"] = True if user_id and item.user_id == user_id else False
    return result


@app.route("/categories/<int:category_id>/items", methods=["POST"])
@jwt_required()
@parse_data()
@load_request_data_by_schema(ItemSchema(exclude=("user_id", "category_id",)))
def add_item(category_id, user_id, category, request_data):
    if Item.find_by_title(request_data["title"]):
        return {"message": "Duplicated item title"}, 400

    item = Item(title=request_data["title"],
                description=request_data["description"],
                user_id=user_id,
                category_id=category_id)
    item.save_to_db()

    item_dump = dump_simple_item(item)
    result = {"message": "Item added", "item": item_dump}
    return result, 201


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["PUT"])
@jwt_required()
@parse_data()
@load_request_data_by_schema(ItemSchema(exclude=("user_id",)))
def update_item_info(category_id, item_id, user_id, category, item, request_data):
    new_category = Category.find_by_id(request_data["category_id"])

    if new_category is None:
        return {"message": "Invalid new category id"}, 400

    if Item.find_by_title(request_data["title"]):
        return {"message": "Duplicated item title"}, 400

    item.title = request_data["title"]
    item.description = request_data["description"]
    item.category_id = request_data["category_id"]
    item.save_to_db()

    item_dump = dump_simple_item(item)
    result = {"message": "Item updated", "item": item_dump}
    return result


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["DELETE"])
@jwt_required()
@parse_data()
def delete_item_info(category_id, item_id, user_id, category, item):
    item.delete_on_db()

    item_dump = dump_simple_item(item)
    result = {"message": "Item deleted", "item": item_dump}
    return result
