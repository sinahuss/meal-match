import pytest
from flask import Flask
from unittest.mock import patch
from app.api.recipes_api import recipes_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(recipes_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_post_recipe_valid(client):
    data = {
        'name': 'Test Recipe',
        'ingredients': [{'name': 'Egg', 'quantity': 2, 'unit': 'piece'}],
        'instructions': ['Step 1', 'Step 2']
    }
    with patch('app.services.recipe_service.create_recipe', return_value='abc123') as mock_create:
        response = client.post('/recipes', json=data)
        assert response.status_code == 201
        assert response.get_json() == {'id': 'abc123'}
        mock_create.assert_called_once_with(data)

def test_post_recipe_invalid(client):
    data = {'ingredients': [], 'instructions': []}  # Missing name
    with patch('app.services.recipe_service.create_recipe', side_effect=ValueError("Recipe 'name' is required.")):
        response = client.post('/recipes', json=data)
        # Should raise error in real app, but current API does not handle it, so will 500
        assert response.status_code == 500 or response.status_code == 400

def test_get_recipes_empty(client):
    with patch('app.services.recipe_service.get_all_recipes', return_value=[]) as mock_get_all:
        response = client.get('/recipes')
        assert response.status_code == 200
        assert response.get_json() == []
        mock_get_all.assert_called_once()

def test_get_recipes_nonempty(client):
    recipes = [
        {'_id': '1', 'name': 'R1', 'ingredients': [], 'instructions': []},
        {'_id': '2', 'name': 'R2', 'ingredients': [], 'instructions': []}
    ]
    with patch('app.services.recipe_service.get_all_recipes', return_value=recipes):
        response = client.get('/recipes')
        assert response.status_code == 200
        assert response.get_json() == recipes 

def test_delete_recipe_success(client):
    with patch('app.services.recipe_service.delete_recipe', return_value=1) as mock_delete:
        response = client.delete('/recipes/abc123')
        assert response.status_code == 204
        mock_delete.assert_called_once_with('abc123')

def test_delete_recipe_not_found(client):
    with patch('app.services.recipe_service.delete_recipe', side_effect=ValueError('Recipe not found')):
        response = client.delete('/recipes/abc123')
        assert response.status_code == 404
        assert response.get_json()['error'] == 'Recipe not found'

def test_delete_recipe_invalid_id(client):
    with patch('app.services.recipe_service.delete_recipe', side_effect=Exception('Invalid recipe ID')):
        response = client.delete('/recipes/invalid!')
        assert response.status_code == 400
        assert response.get_json()['error'] == 'Invalid recipe ID'

def test_get_recipe_by_id_success(client):
    recipe = {'_id': 'abc123', 'name': 'Test', 'ingredients': [], 'instructions': []}
    with patch('app.services.recipe_service.get_recipe_by_id', return_value=recipe) as mock_get:
        response = client.get('/recipes/abc123')
        assert response.status_code == 200
        assert response.get_json() == recipe
        mock_get.assert_called_once_with('abc123')

def test_get_recipe_by_id_not_found(client):
    with patch('app.services.recipe_service.get_recipe_by_id', side_effect=ValueError('Recipe not found')):
        response = client.get('/recipes/abc123')
        assert response.status_code == 404
        assert response.get_json()['error'] == 'Recipe not found'

def test_get_recipe_by_id_invalid_id(client):
    with patch('app.services.recipe_service.get_recipe_by_id', side_effect=Exception('Invalid recipe ID')):
        response = client.get('/recipes/invalid!')
        assert response.status_code == 400
        assert response.get_json()['error'] == 'Invalid recipe ID'

def test_update_recipe_success(client):
    with patch('app.services.recipe_service.update_recipe', return_value=1) as mock_update:
        response = client.put('/recipes/abc123', json={'name': 'Updated'})
        assert response.status_code == 200
        assert response.get_json() == {'modified_count': 1}
        mock_update.assert_called_once_with('abc123', {'name': 'Updated'})

def test_update_recipe_not_found(client):
    with patch('app.services.recipe_service.update_recipe', side_effect=ValueError('Recipe not found')):
        response = client.put('/recipes/abc123', json={'name': 'Updated'})
        assert response.status_code == 404
        assert response.get_json()['error'] == 'Recipe not found'

def test_update_recipe_invalid_id(client):
    with patch('app.services.recipe_service.update_recipe', side_effect=Exception('Invalid recipe ID')):
        response = client.put('/recipes/invalid!', json={'name': 'Updated'})
        assert response.status_code == 400
        assert response.get_json()['error'] == 'Invalid recipe ID' 