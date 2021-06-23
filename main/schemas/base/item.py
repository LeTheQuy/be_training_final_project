from marshmallow import Schema, fields, validate, pre_load, post_dump


class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=[validate.Length(min=1, max=45)])
    description = fields.Str(required=True, validate=[validate.Length(min=10, max=1000)])
    category_id = fields.Int(required=True, validate=validate.Range(min=0))
    user_id = fields.Int(required=True, validate=validate.Range(min=0))

    user = fields.Nested("UserSchema", exclude={"items"}, dump_only=True)
    category = fields.Nested("CategorySchema", exclude={"items"}, dump_only=True)

    @pre_load
    def process_input(self, data, **kwargs):
        data["title"] = data["title"].lower().strip()
        data["description"] = data["description"].strip()
        return data

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {"items: data"}
        return data
