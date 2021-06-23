from marshmallow import Schema, fields, validate


class ParserSchema(Schema):
    category_id = fields.Integer(validate=validate.Range(min=0))
    item_id = fields.Integer(validate=validate.Range(min=0))
    user_id = fields.Integer(validate=validate.Range(min=0))
