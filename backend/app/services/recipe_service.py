from app.db.mongo_setup import get_db_instance
from bson.objectid import ObjectId


def create_recipe(data):
    # Basic validation (customize as needed)
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
