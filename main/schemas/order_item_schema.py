from marshmallow import Schema, fields, validate, post_load

from main.config.config import config
from main.models.item import Item


class OrderItemSchema(Schema):
    order = fields.Str(required=False, validate=validate.OneOf([None, "newest"]))
    items_per_page = fields.Integer(required=False, default=config.ITEM_PER_PAGE)

    @post_load(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if "order" in data and "items_per_page" in data:
            return Item.get_latest_added_list(data["items_per_page"])
        return Item.find_all(data["items_per_page"])