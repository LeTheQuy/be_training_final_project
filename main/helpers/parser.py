import functools

from marshmallow import ValidationError

from main.models.category import Category
from main.models.item import Item
from main.schemas.parser_schema import ParserSchema


def parse_category():
    def decorator_parser_category(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            try:
                data = ParserSchema().dump(kwargs)
            except ValidationError as err:
                return {"message": err.messages}, 400
            if "category_id" in data:
                category = Category.find_by_id(data["category_id"])
                kwargs["category"] = category
                if not category:
                    return {"message": "Invalid category id"}, 400
            return f(*args, **kwargs)

        return decorated

    return decorator_parser_category


def parse_item():
    def decorator_parser_item(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            try:
                data = ParserSchema().dump(kwargs)
            except ValidationError as err:
                return {"message": err.messages}, 400
            if "item_id" in data:
                item = Item.find_by_id(data["item_id"])
                kwargs["item"] = item
                if not item:
                    return {"message": "Invalid item id"}, 400
            if kwargs["category"] and item.category_id != kwargs["category"].id:
                return {"message": "Category and item don't match"}, 400

            return f(*args, **kwargs)

        return decorated

    return decorator_parser_item


def parse_editable_item():
    def decorator_editable_item(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            editable = False
            if "user_id" in kwargs and kwargs["item"] and kwargs["item"].user_id == kwargs["user_id"]:
                editable = True
            kwargs["editable"] = editable
            return f(*args, **kwargs)

        return decorated

    return decorator_editable_item
