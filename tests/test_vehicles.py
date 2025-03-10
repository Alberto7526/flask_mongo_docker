import json
import pytest
from app import app
from bson import ObjectId


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_vehicles(client):
    response = client.get("/vehicles")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_get_vehicle_by_id(client):
    new_vehicle = {"placa": "ABC124", "tipo": "Sedán"}

    response = client.post("/vehicles", json=new_vehicle)
    assert response.status_code == 201
    vehicle_id = json.loads(response.data)["id"]
    response = client.get(f"/vehicles/{vehicle_id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "_id" in data
    assert "placa" in data
    assert "tipo" in data
    assert "disponibilidad" in data
    assert ObjectId(vehicle_id) == ObjectId(data["_id"]["$oid"])

    # Borrar el vehículo después de la prueba
    response = client.delete(f"/vehicles/{vehicle_id}")
    assert response.status_code == 204


def test_create_vehicle_duplicate_plate(client):
    new_vehicle_1 = {"placa": "DEF456", "tipo": "SUV"}
    response = client.post("/vehicles", json=new_vehicle_1)
    assert response.status_code == 201
    vehicle_id_1 = json.loads(response.data)["id"]

    # Crear otro vehículo con la misma placa
    new_vehicle_2 = {"placa": "DEF456", "tipo": "Coupé"}
    response = client.post("/vehicles", json=new_vehicle_2)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert "Vehicle already exists" in data["error"]

    # Borrar el vehículo después de la prueba
    response = client.delete(f"/vehicles/{vehicle_id_1}")
    assert response.status_code == 204


def test_update_vehicle(client):
    new_vehicle = {"placa": "LMN321", "tipo": "Hatchback"}
    response = client.post("/vehicles", json=new_vehicle)
    assert response.status_code == 201
    vehicle_id = json.loads(response.data)["id"]

    updated_vehicle = {"placa": "LMN321", "tipo": "Hatchback", "disponibilidad": False}
    response = client.put(f"/vehicles/{vehicle_id}", json=updated_vehicle)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "id" in data
    assert data["id"]["$oid"] == vehicle_id

    response = client.get(f"/vehicles/{vehicle_id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["disponibilidad"] is False

    # Borrar el vehículo después de la prueba
    response = client.delete(f"/vehicles/{vehicle_id}")
    assert response.status_code == 204


def test_delete_vehicle(client):
    new_vehicle = {"placa": "GHI987", "tipo": "Camioneta"}
    response = client.post("/vehicles", json=new_vehicle)
    assert response.status_code == 201
    vehicle_id = json.loads(response.data)["id"]
    response = client.delete(f"/vehicles/{vehicle_id}")
    assert response.status_code == 204
    # Verificar que el vehículo ha sido eliminado
    response = client.get(f"/vehicles/{vehicle_id}")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "Vehicle not found" in data["error"]
