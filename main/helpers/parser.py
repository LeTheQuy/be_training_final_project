import functools

from marshmallow import ValidationError

from main.models.category import Category
from main.models.item import Item
from main.schemas.parser_schema import ParserSchema


def parse_data(check_editable=True):
    def decorator_parser(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            try:
                data = ParserSchema().dump(kwargs)
            except ValidationError as err:
                return {"message": err.messages}, 400
            category, item = None, None
            if "category_id" in data:
                category = Category.find_by_id(data["category_id"])
                kwargs["category"] = category
                if not category:
                    return {"message": "Invalid category id"}, 400
            if "item_id" in data:
                item = Item.find_by_id(data["item_id"])
                kwargs["item"] = item
                if not item:
                    return {"message": "Invalid item id"}, 400
            if item and category and item.category_id != category.id:
                return {"message": "Category and item don't match"}, 400

            if check_editable and "user_id" in data and item and item.user_id != data["user_id"]:
                return {"message": "This item is not editable by yourself"}, 403
            return f(*args, **kwargs)

        return decorated

    return decorator_parser
