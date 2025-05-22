import pytest
from marshmallow import ValidationError
from app.models.recipe_model import RecipeSchema

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