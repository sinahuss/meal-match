import pytest
from unittest.mock import patch, MagicMock
from app.db import mongo_setup

# Test init_db for successful connection
@patch('app.db.mongo_setup.MongoClient')
def test_init_db_success(mock_mongo_client):
    mock_client = MagicMock()
    mock_db = MagicMock()
    mock_mongo_client.return_value = mock_client
    mock_client.__getitem__.return_value = mock_db
    app_config = {'MONGO_URI': 'uri', 'MONGO_DBNAME': 'testdb'}
    db = mongo_setup.init_db(app_config)
    assert db == mock_db

# Test init_db for failed connection
@patch('app.db.mongo_setup.MongoClient', side_effect=Exception('Connection failed'))
def test_init_db_failure(mock_mongo_client):
    mongo_setup.client = None
    mongo_setup.db = None
    app_config = {'MONGO_URI': 'uri', 'MONGO_DBNAME': 'testdb'}
    with pytest.raises(Exception) as excinfo:
        mongo_setup.init_db(app_config)
    assert 'Connection failed' in str(excinfo.value)

# Test get_db_client and get_db_instance for uninitialized state
@patch('app.db.mongo_setup.client', None)
def test_get_db_client_uninitialized():
    with pytest.raises(Exception) as excinfo:
        mongo_setup.get_db_client()
    assert 'MongoDB client not initialized' in str(excinfo.value)

@patch('app.db.mongo_setup.db', None)
def test_get_db_instance_uninitialized():
    with pytest.raises(Exception) as excinfo:
        mongo_setup.get_db_instance()
    assert 'MongoDB database instance not initialized' in str(excinfo.value)

# Test ensure_indexes error handling
@patch('app.db.mongo_setup.get_db_instance', side_effect=Exception('Index error'))
def test_ensure_indexes_error(mock_get_db):
    result = mongo_setup.ensure_indexes()
    assert 'error' in result and 'Index error' in result['error'] 