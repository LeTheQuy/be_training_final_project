from marshmallow import Schema, fields, validate, pre_load, post_dump

from main.schemas.validation import must_not_be_blank


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=[must_not_be_blank, validate.Length(min=0, max=45)])
    items = fields.List(fields.Nested("ItemSchema", exclude=("user", "category",), dump_only=True))

    @pre_load
    def process_input(self, data, **kwargs):
        data["name"] = data["name"].lower().strip()
        return data

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        key = "categories" if many else "category"
        return {key: data}
