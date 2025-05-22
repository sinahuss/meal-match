import pytest
from app import create_app
from flask import Flask
from unittest.mock import patch

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_app_default():
    app = create_app()
    assert isinstance(app, Flask)
    assert app.name == 'app'

def test_health_check_ok(client):
    with patch('app.db.mongo_setup.get_db_instance', return_value=True):
        response = client.get('/health')
        assert response.status_code == 200
        assert 'Flask App: OK, MongoDB: OK' in response.get_data(as_text=True)

def test_health_check_unavailable(client):
    with patch('app.db.mongo_setup.get_db_instance', return_value=None):
        response = client.get('/health')
        assert response.status_code == 200
        assert 'MongoDB: Unavailable' in response.get_data(as_text=True) 