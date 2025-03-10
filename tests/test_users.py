import json
import pytest
from app import app
from bson import ObjectId


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_get_user_by_id(client):
    new_user = {"nombre": "Pepito Son", "email": "pepito.son@example.com"}

    response = client.post("/users", json=new_user)
    assert response.status_code == 201
    user_id = json.loads(response.data)["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "_id" in data
    assert "nombre" in data
    assert "email" in data
    assert "historial_reservas" in data
    assert ObjectId(user_id) == ObjectId(data["_id"]["$oid"])

    # Borrar el usuario después de la prueba
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204


def test_create_user_invalid_email(client):
    new_user = {"nombre": "Ana García", "email": "invalid-email"}

    response = client.post("/users", json=new_user)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert "Invalid email" in data["error"]


def test_create_user_duplicate_email(client):
    new_user_1 = {"nombre": "Carlos López", "email": "carlos.lopez@example.com"}
    response = client.post("/users", json=new_user_1)
    assert response.status_code == 201
    user_id_1 = json.loads(response.data)["id"]

    # creamos otro usuario pero con el mismo email
    new_user_2 = {"nombre": "Juan Pérez", "email": "carlos.lopez@example.com"}
    response = client.post("/users", json=new_user_2)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert "Email already exists" in data["error"]

    # Borrar el usuario después de la prueba
    response = client.delete(f"/users/{user_id_1}")
    assert response.status_code == 204


def test_update_user(client):
    new_user = {"nombre": "Luis Gómez", "email": "luis.gomez@example.com"}
    response = client.post("/users", json=new_user)
    assert response.status_code == 201
    user_id = json.loads(response.data)["id"]

    updated_user = {"nombre": "Luis Gómez", "email": "luis.gomez_new@example.com"}
    response = client.put(f"/users/{user_id}", json=updated_user)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "id" in data
    assert data["id"] == user_id

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["email"] == "luis.gomez_new@example.com"

    # Borrar el usuario después de la prueba
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
