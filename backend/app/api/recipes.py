from flask import Blueprint, request, jsonify
from app.services.recipe_service import create_recipe

recipes_bp = Blueprint("recipes", __name__, url_prefix="/recipes")


@recipes_bp.route("", methods=["POST"])
def add_recipe():
    data = request.get_json()
    recipe_id = create_recipe(data)
    return jsonify({"id": recipe_id}), 201
