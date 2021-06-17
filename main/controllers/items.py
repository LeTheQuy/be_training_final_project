from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from main.app import app


@app.route("/items?", methods=["GET"])
def get_latest_added_items():
    if request.args.get("order"):
        if request.args.get("limit"):
            pass
        else:
            return
    else:
        if request.args.get("limit"):
            pass
        else:
            return


@app.route("/categories/<int:category_id>/items")
def get_items_by_category_id(category_id):
    page = int(request.args.get("page"))
    limit = int(request.args.get("limit"))


@jwt_required(optional=True)
@app.route("/categories/<int:category_id>/items/<int:item_id>")
def get_item_detail(category_id, item_id):
    user_id = get_jwt_identity()
    if user_id:
        pass
    else:
        pass


@jwt_required()
@app.route("/categories/<int:category_id>/items", methods=["POST"])
def add_item(category_id):
    pass


@jwt_required()
@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["PUT"])
def update_item_info(category_id, item_id):
    pass


@jwt_required()
@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["DELETE"])
def delete_item_info(category_id, item_id):
    pass
