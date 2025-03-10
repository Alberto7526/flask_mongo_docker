import json
import pytest
from config.config import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Test para obtener todos los usuarios
def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200
