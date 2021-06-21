from marshmallow import ValidationError

from main.models.category import Category


def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")


def exist_category(category_id):
    if Category.find_by_id(category_id) is None:
        raise ValidationError("Invalid category id")
