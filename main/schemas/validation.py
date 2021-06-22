import functools

from flask import request
from marshmallow import ValidationError

from main.models.category import Category
from main.models.item import Item


def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")


def exist_category(category_id):
    if Category.find_by_id(category_id) is None:
        raise ValidationError("Invalid category id")


def exist_item(item_id):
    if Item.find_by_id(item_id) is None:
        raise ValidationError("Invalid item id")


def load_request_data_by_schema(schema):
    def decorator_schema(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            if request.method == "GET":
                request_data = request.args.to_dict()
            else:
                request_data = request.get_json()
            try:
                request_data = schema.load(request_data)
            except ValidationError as err:
                return {"message": err.messages}, 400
            kwargs['request_data'] = request_data
            return f(*args, **kwargs)

        return decorated

    return decorator_schema
