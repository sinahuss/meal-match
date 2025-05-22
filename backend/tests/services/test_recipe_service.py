import pytest
from unittest.mock import patch, MagicMock
from app.services.recipe_service import create_recipe, get_all_recipes
from app.db.mongo_setup import ensure_indexes

@patch('app.services.recipe_service.get_db_instance')
def test_create_recipe_valid(mock_get_db):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    mock_result = MagicMock(inserted_id='123')
    mock_db.recipes.insert_one.return_value = mock_result

    data = {
        'name': 'Test Recipe',
        'ingredients': [
            {'name': 'Egg', 'quantity': 2, 'unit': 'piece'}
        ],
        'instructions': ['Step 1', 'Step 2']
    }
    recipe_id = create_recipe(data)
    assert recipe_id == '123'
    mock_db.recipes.insert_one.assert_called_once_with(data)

@patch('app.services.recipe_service.get_db_instance')
def test_create_recipe_missing_name(mock_get_db):
    data = {
        'ingredients': [{'name': 'Egg', 'quantity': 2, 'unit': 'piece'}],
        'instructions': ['Step 1', 'Step 2']
    }
    with pytest.raises(ValueError):
        create_recipe(data)

def test_ensure_indexes_success():
    mock_db = MagicMock()
    mock_db.recipes.index_information.return_value = {"_id_": {"key": [('_id', 1)]}}
    with patch('app.db.mongo_setup.get_db_instance', return_value=mock_db):
        result = ensure_indexes()
        assert isinstance(result, list)
        # Check that create_indexes was called once with a list of IndexModel objects
        args, kwargs = mock_db.recipes.create_indexes.call_args
        from pymongo import IndexModel
        assert len(args) == 1
        assert all(isinstance(idx, IndexModel) for idx in args[0])

def test_ensure_indexes_error():
    with patch('app.db.mongo_setup.get_db_instance', side_effect=Exception("DB error")):
        result = ensure_indexes()
        assert "error" in result

def test_get_all_recipes_empty():
    mock_db = MagicMock()
    mock_db.recipes.find.return_value = []
    with patch('app.services.recipe_service.get_db_instance', return_value=mock_db):
        recipes = get_all_recipes()
        assert recipes == []
        mock_db.recipes.find.assert_called_once()

def test_get_all_recipes_nonempty():
    mock_db = MagicMock()
    mock_db.recipes.find.return_value = [{'_id': 1, 'name': 'R1'}, {'_id': 2, 'name': 'R2'}]
    with patch('app.services.recipe_service.get_db_instance', return_value=mock_db):
        recipes = get_all_recipes()
        assert recipes[0]['_id'] == '1'
        assert recipes[1]['_id'] == '2'
        mock_db.recipes.find.assert_called_once()

def test_create_recipe_db_error():
    with patch('app.services.recipe_service.get_db_instance', side_effect=Exception('DB error')):
        with pytest.raises(Exception) as excinfo:
            create_recipe({'name': 'fail', 'ingredients': [], 'instructions': []})
        assert 'DB error' in str(excinfo.value) 