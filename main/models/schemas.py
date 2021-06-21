from marshmallow import Schema, fields, pre_load, validate, post_dump

from main.helpers.validation import must_not_be_blank, exist_category


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(
        required=True, validate=validate.Email(error="Not a valid email address")
    )
    password = fields.Str(
        required=True, validate=[validate.Length(min=6, max=36)], load_only=True
    )

    items = fields.List(fields.Nested("ItemSchema", exclude=("user", "category",), dump_only=True))

    @pre_load
    def process_input(self, data, **kwargs):
        data["username"] = data["username"].lower().strip()
        data["password"] = data["password"].strip()
        return data


user_schema = UserSchema(exclude=("items",))


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


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True, only=("id", "name"))


class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=[must_not_be_blank, validate.Length(min=0, max=45)])
    description = fields.Str(required=True, validate=[must_not_be_blank, validate.Length(min=0, max=1000)])
    category_id = fields.Int(required=False, validate=[exist_category], load_only=True)
    user = fields.Nested(UserSchema, dump_only=True)
    category = fields.Nested(CategorySchema, dump_only=True)

    @pre_load
    def process_input(self, data, **kwargs):
        data["title"] = data["title"].lower().strip()
        data["description"] = data["description"].strip()
        return data

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        key = "items" if many else "item"
        return {key: data}


item_schema = ItemSchema(only=("id", "title", "description", "category_id", "category.id", "category.name"))

items_schema = ItemSchema(many=True, only=("id", "title", "description", "category.id", "category.name"))
