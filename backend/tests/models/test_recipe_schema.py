import pytest
from marshmallow import ValidationError
from app.models.recipe_model import RecipeSchema, IngredientSchema, NutritionalInfoSchema

def test_recipe_schema_valid():
    data = {
        'name': 'Test Recipe',
        'ingredients': [{'name': 'Egg', 'quantity': 2, 'unit': 'piece'}],
        'instructions': ['Step 1', 'Step 2']
    }
    result = RecipeSchema().load(data)
    assert result['name'] == 'Test Recipe'
    assert isinstance(result['ingredients'], list)
    assert isinstance(result['instructions'], list)

def test_recipe_schema_missing_name():
    data = {
        'ingredients': [{'name': 'Egg', 'quantity': 2, 'unit': 'piece'}],
        'instructions': ['Step 1', 'Step 2']
    }
    with pytest.raises(ValidationError):
        RecipeSchema().load(data)

def test_recipe_schema_invalid_ingredient():
    data = {
        'name': 'Test Recipe',
        'ingredients': [{'quantity': 2, 'unit': 'piece'}],  # Missing name
        'instructions': ['Step 1', 'Step 2']
    }
    with pytest.raises(ValidationError):
        RecipeSchema().load(data)

def test_recipe_schema_invalid_nutritional_info():
    data = {
        'name': 'Test Recipe',
        'ingredients': [{'name': 'Egg', 'quantity': 2, 'unit': 'piece'}],
        'instructions': ['Step 1', 'Step 2'],
        'nutritional_info': {'calories': 'a lot'}  # Invalid type
    }
    with pytest.raises(ValidationError):
        RecipeSchema().load(data)

def test_recipe_schema_extra_fields():
    data = {
        'name': 'Test Recipe',
        'ingredients': [{'name': 'Egg', 'quantity': 2, 'unit': 'piece'}],
        'instructions': ['Step 1', 'Step 2'],
        'extra_field': 'should be ignored'
    }
    with pytest.raises(ValidationError):
        RecipeSchema().load(data)

def test_ingredient_schema_required_fields():
    with pytest.raises(ValidationError):
        IngredientSchema().load({'quantity': 2, 'unit': 'piece'})  # Missing name
    with pytest.raises(ValidationError):
        IngredientSchema().load({'name': 'Egg', 'unit': 'piece'})  # Missing quantity
    with pytest.raises(ValidationError):
        IngredientSchema().load({'name': 'Egg', 'quantity': 2})  # Missing unit 