from flask import Blueprint, request, jsonify
import app.services.recipe_service as recipe_service

recipes_bp = Blueprint("recipes", __name__, url_prefix="/recipes")

# GET all recipes
@recipes_bp.route("", methods=["GET"])
def get_recipes():
    recipes = recipe_service.get_all_recipes()
    return jsonify(recipes), 200

# POST a new recipe
@recipes_bp.route("", methods=["POST"])
def add_recipe():
    data = request.get_json()
    recipe_id = recipe_service.create_recipe(data)
    return jsonify({"id": recipe_id}), 201

# GET a single recipe by ID
@recipes_bp.route("/<recipe_id>", methods=["GET"])
def get_recipe_by_id_endpoint(recipe_id):
    try:
        recipe = recipe_service.get_recipe_by_id(recipe_id)
        return jsonify(recipe), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Invalid recipe ID'}), 400

# PUT (update) a recipe by ID
@recipes_bp.route("/<recipe_id>", methods=["PUT"])
def update_recipe_endpoint(recipe_id):
    data = request.get_json()
    try:
        modified_count = recipe_service.update_recipe(recipe_id, data)
        return jsonify({'modified_count': modified_count}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Invalid recipe ID'}), 400

# DELETE a recipe by ID
@recipes_bp.route("/<recipe_id>", methods=["DELETE"])
def delete_recipe_endpoint(recipe_id):
    try:
        deleted_count = recipe_service.delete_recipe(recipe_id)
        return '', 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Invalid recipe ID'}), 400
