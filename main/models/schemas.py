from marshmallow import Schema, fields, pre_load, validate, post_dump

from main.helpers.validation import must_not_be_blank


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(
        required=True, validate=validate.Email(error="Not a valid email address")
    )
    password = fields.Str(
        required=True, validate=[validate.Length(min=6, max=36)], load_only=True
    )

    @pre_load
    def process_input(self, data, **kwargs):
        data["username"] = data["username"].lower().strip()
        data["password"] = data["password"].strip()
        return data

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        key = "users" if many else "user"
        return {key: data}


user_schema = UserSchema()


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=must_not_be_blank)

    @pre_load
    def process_input(self, data, **kwargs):
        data["name"] = data["name"].lower().strip()
        return data


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True, only=("id", "name"))


class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=must_not_be_blank)
    description = fields.Str(required=True, validate=must_not_be_blank)
    user = fields.Nested(UserSchema, validate=must_not_be_blank, dump_only=True)
    category = fields.Nested(CategorySchema, validate=must_not_be_blank, dump_only=True)

    @pre_load
    def process_input(self, data, **kwargs):
        data["title"] = data["title"].lower().strip()
        data["description"] = data["description"].strip()
        return data


item_schema = ItemSchema()
items_schema = ItemSchema(many=True, only=("id", "title", "description"))
