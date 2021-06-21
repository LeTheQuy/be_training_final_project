from marshmallow import Schema, fields, validate, pre_load, post_dump

from main.schemas.validation import must_not_be_blank, exist_category


class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=[must_not_be_blank, validate.Length(min=0, max=45)])
    description = fields.Str(required=True, validate=[must_not_be_blank, validate.Length(min=0, max=1000)])
    category_id = fields.Int(required=False, validate=[exist_category], load_only=True)
    user = fields.Nested("UserSchema", dump_only=True)
    category = fields.Nested("CategorySchema", dump_only=True)

    @pre_load
    def process_input(self, data, **kwargs):
        data["title"] = data["title"].lower().strip()
        data["description"] = data["description"].strip()
        return data

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        key = "items" if many else "item"
        return {key: data}
