from flask import Blueprint, request, jsonify
from app.services.recipe_service import create_recipe, get_all_recipes, delete_recipe

recipes_bp = Blueprint("recipes", __name__, url_prefix="/recipes")


@recipes_bp.route("", methods=["POST"])
def add_recipe():
    data = request.get_json()
    recipe_id = create_recipe(data)
    return jsonify({"id": recipe_id}), 201

@recipes_bp.route("", methods=["GET"])
def get_recipes():
    recipes = get_all_recipes()
    return jsonify(recipes), 200

@recipes_bp.route("/<recipe_id>", methods=["DELETE"])
def delete_recipe_endpoint(recipe_id):
    try:
        deleted_count = delete_recipe(recipe_id)
        return '', 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Invalid recipe ID'}), 400
