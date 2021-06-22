from marshmallow import Schema, fields, post_load, ValidationError

from main.models.item import Item
from main.schemas.validation import exist_category, exist_item


class CategoryItemSchema(Schema):
    category_id = fields.Integer(required=True, validate=[exist_category])
    item_id = fields.Integer(required=True, validate=[exist_item])
    user_id = fields.Integer(required=True)

    @post_load
    def process_input(self, data, **kwargs):
        item = Item.find_by_id(data["item_id"])
        if item.category_id != data["category_id"]:
            raise ValidationError("Category and item don't match")
        if data["user_id"] is not None and item.user_id != data["user_id"]:
            raise ValidationError("This item is not editable by yourself")
        return data

    @post_load(pass_many=True)
    def wrap(self, data, many, **kwargs):
        return Item.find_by_id(data["item_id"])


def get_item_by_condition(**kwargs):
    category_item_schema = CategoryItemSchema()
    return category_item_schema.load(kwargs)