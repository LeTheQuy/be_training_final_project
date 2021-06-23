from marshmallow import Schema, fields, validate, post_load

from main.config.config import config


class PaginationSchema(Schema):
    order = fields.Str(required=False, validate=validate.OneOf(["newest"]))
    page = fields.Integer(required=False, validate=validate.Range(min=1))
    items_per_page = fields.Integer(required=False,
                                    validate=validate.Range(min=1, max=100))

    @post_load(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if "items_per_page" not in data:
            data["items_per_page"] = config.ITEMS_PER_PAGE
        if "page" not in data:
            data["page"] = 1
        return data
