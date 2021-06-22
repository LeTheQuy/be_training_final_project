from marshmallow import Schema, fields

from main.config.config import config


class PaginationSchema(Schema):
    page = fields.Integer(required=False, default=1)
    items_per_page = fields.Integer(required=False, default=config.ITEM_PER_PAGE)