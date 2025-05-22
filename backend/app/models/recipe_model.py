from marshmallow import Schema, fields, validate

class IngredientSchema(Schema):
    name = fields.String(required=True)
    quantity = fields.Raw(required=True)  # Accepts float or string
    unit = fields.String(required=True)
    preparation_notes = fields.String(load_default=None)

class NutritionalInfoSchema(Schema):
    calories = fields.Integer(load_default=None)
    protein_grams = fields.Float(load_default=None)
    fat_grams = fields.Float(load_default=None)
    carb_grams = fields.Float(load_default=None)

class RecipeSchema(Schema):
    _id = fields.String(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(load_default=None)
    ingredients = fields.List(fields.Nested(IngredientSchema), required=True)
    instructions = fields.List(fields.String, required=True)
    cuisine_type = fields.String(load_default=None)
    dish_type = fields.String(load_default=None)
    prep_time_minutes = fields.Integer(load_default=None)
    cook_time_minutes = fields.Integer(load_default=None)
    servings = fields.Integer(load_default=None)
    nutritional_info = fields.Nested(NutritionalInfoSchema, load_default=None)
    tags = fields.List(fields.String, load_default=None)
    source_url = fields.String(load_default=None)
    image_url = fields.String(load_default=None)
    created_at = fields.DateTime(load_default=None, dump_only=True)
    updated_at = fields.DateTime(load_default=None, dump_only=True)
    search_keywords = fields.List(fields.String, load_default=None)
