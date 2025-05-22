from app.db.mongo_setup import get_db_instance
from bson.objectid import ObjectId


def create_recipe(data):
    # Basic validation
    if not data or 'name' not in data:
        raise ValueError("Recipe 'name' is required.")

    db = get_db_instance()
    result = db.recipes.insert_one(data)
    return str(result.inserted_id)

def get_all_recipes():
    db = get_db_instance()
    recipes = list(db.recipes.find())
    for recipe in recipes:
        recipe["_id"] = str(recipe["_id"])
    return recipes

def get_recipe_by_id(recipe_id):
    db = get_db_instance()
    recipe = db.recipes.find_one({"_id": ObjectId(recipe_id)})
    if not recipe:
        raise ValueError("Recipe not found")
    recipe["_id"] = str(recipe["_id"])
    return recipe

def delete_recipe(recipe_id):
    db = get_db_instance()
    result = db.recipes.delete_one({"_id": ObjectId(recipe_id)})
    if result.deleted_count == 0:
        raise ValueError("Recipe not found")
    return result.deleted_count

def update_recipe(recipe_id, data):
    db = get_db_instance()
    result = db.recipes.update_one({"_id": ObjectId(recipe_id)}, {"$set": data})
    if result.matched_count == 0:
        raise ValueError("Recipe not found")
    return result.modified_count
