from marshmallow import Schema, fields, validate, pre_load


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Email(error="Not a valid email address"))
    password = fields.Str(required=True, validate=[validate.Length(min=6, max=36)], load_only=True)
    items = fields.List(fields.Nested("ItemSchema", exclude=("user", "category",), dump_only=True))

    @pre_load
    def process_input(self, data, **kwargs):
        data["username"] = data["username"].lower().strip()
        data["password"] = data["password"].strip()
        return data
