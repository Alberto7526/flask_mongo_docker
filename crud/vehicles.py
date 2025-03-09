from config.config import mongo
from bson.json_util import dumps
from bson import ObjectId
from flask import Response, jsonify


def get_vehicles():
    """
    Obtiene todos los vehiculos de la base de datos.

    Returns:
        list[vehicle]: Una lista de todos los vehicles registrados.

    Raises:
        HTTPException:
            - 500: Si ocurre un error inesperado al obtener los vehicles.
    """
    vehicles = mongo.db.vehiculos.find()
    vehicles = dumps(vehicles)
    return Response(vehicles, mimetype="application/json", status=200)


def get_vehicle_by_id(id):
    """
    Obtiene un vehiculo por su ID

    Args:
        id (str): ID del vehiculo a buscar.

    returns:
        vehicle: El objeto del vehiculo correspondiente al ID.

    Raises:
        HTTPException:
            - 404: Si el vehiculo no se encuentra en la base de datos.

    """
    try:
        id = ObjectId(id)
    except Exception as e:
        message = {"error": "Invalid ID", "message": str(e)}
        return jsonify(message), 400
    vehicle = mongo.db.vehiculos.find_one({"_id": ObjectId(id)})
    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404
    vehicle = dumps(vehicle)
    return Response(vehicle, mimetype="application/json", status=200)


def create_vehicle(vehicle):
    """
    Crea un nuevo vehiculo en la base de datos.

    Args:
        vehicle (dict): Un diccionario con los datos del vehiculo a crear, debe incluir tipo, placa.

    returns:
        vehicle: El objeto del vehiculo creado.

    Raises:
        HTTPException:
            - 400: Si el vehiculo ya existe o el Id es invalido.
            - 500: Si ocurre un error inesperado al crear el vehiculo.
    """
    placa = vehicle.get("placa")
    tipo = vehicle.get("tipo")
    if placa is None or tipo is None:
        return (
            jsonify(
                {
                    "error": "Missing required fields, please ensure your data includes 'placa' and 'tipo'"
                }
            ),
            400,
        )
    if mongo.db.vehiculos.find_one({"placa": placa}):
        return jsonify({"error": "Vehicle already exists"}), 400
    vehiculo = {"placa": placa, "tipo": tipo, "disponible": True}
    vehicle_id = mongo.db.vehiculos.insert_one(vehiculo)
    return jsonify({"id": str(vehicle_id.inserted_id)}), 201


def update_vehicle(id, vehicle):
    """
    Actualiza un vehiculo en la base de datos.

    Args:
        id (str): ID del vehiculo a actualizar.
        vehicle (dict): Un diccionario con los datos del vehiculo a actualizar, debe incluir tipo, placa, disponibilidad.

    returns:
        vehicle: El ID objeto del vehiculo actualizado.

    Raises:
        HTTPException:
            - 400: Si el Id es invalido o la placa ya existe.
            - 404: Si el vehiculo no se encuentra en la base de datos.
            - 500: Si ocurre un error inesperado al actualizar el vehiculo.
    """
    try:
        id = ObjectId(id)
    except Exception as e:
        message = {"error": "Invalid ID", "message": str(e)}
        return jsonify(message), 400
    placa = vehicle.get("placa")
    tipo = vehicle.get("tipo")
    disponibilidad = vehicle.get("disponibilidad")
    if placa is None or tipo is None or disponibilidad is None:
        return (
            jsonify(
                {
                    "error": "Missing required fields, please ensure your data includes 'placa', 'tipo' and 'disponibilidad'"
                }
            ),
            400,
        )
    if mongo.db.vehiculos.find_one({"_id": ObjectId(id)}) is None:
        return jsonify({"error": "Vehicle not found"}), 404
    if mongo.db.vehiculos.find_one(
        {"$and": [{"placa": placa}, {"_id": {"$ne": ObjectId(id)}}]}
    ):
        return jsonify({"error": "Vehicle already exists"}), 400
    mongo.db.vehiculos.update_one({"_id": ObjectId(id)}, {"$set": vehicle})
    return jsonify({"id": id}), 200


def delete_vehicle(id):
    """
    Elimina un vehiculo de la base de datos.

    Args:
        id (str): ID del vehiculo a eliminar.

    Returns:
        id: El _id del objeto del vehiculo eliminado.

    Raises:
        HTTPException:
            - 400: Si el ID es inválido.
            - 404: Si el vehiculo no se encuentra en la base de datos.
    """
    try:
        id = ObjectId(id)
    except Exception as e:
        message = {"error": "Invalid ID", "message": str(e)}
        return jsonify(message), 400
    vehicle = mongo.db.vehiculos.find_one({"_id": ObjectId(id)})
    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404
    mongo.db.vehiculos.delete_one({"_id": ObjectId(id)})
    return jsonify({"id": id}), 200
