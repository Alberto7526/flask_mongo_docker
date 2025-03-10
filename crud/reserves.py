from app import mongo
from bson.json_util import dumps
from bson import ObjectId
from flask import Response, jsonify
from datetime import datetime, timedelta
from utils.utils import *


def get_reserves():
    """
    Obtiene todas las reservas de la base de datos.

    Returns:
        list[reservation]: Una lista de todas las reservas registrados.

    Raises:
        HTTPException:
            - 500: Si ocurre un error inesperado al obtener los usuarios.
    """
    reservations = mongo.db.reservas.find()
    reservations = dumps(reservations)
    return Response(reservations, mimetype="application/json", status=200)


def create_reservation(reservation):
    """
    Crea una nueva reserva en la base de datos.

    Args:
        reservation (dict): Un diccionario con los datos de la reserva a crear, debe incluir id_usuario, id_vehiculo, fecha_inicio, fecha_fin.

    returns:
        reservation: El objeto de la reserva creada.

    Raises:
        HTTPException:
            - 400 Si la reserva no se pudo crear.
    """
    user_id = reservation.get("id_usuario")
    vehicle_id = reservation.get("id_vehiculo")
    start_date = reservation.get("fecha_inicio")
    end_date = reservation.get("fecha_fin")

    # Validamos y convertimos los ids
    try:
        user_id = ObjectId(user_id)
        vehicle_id = ObjectId(vehicle_id)
    except Exception as e:
        message = {"error": "Invalid ID", "message": str(e)}
        return jsonify(message), 400

    # Verificamos si existe el usuario
    user = mongo.db.usuarios.find_one({"_id": user_id})
    if user is None:
        return jsonify({"error": "User not found"}), 404

    if user["estado"]:
        return (
            jsonify(
                {
                    "error": "User temporarily blocked from making reservations.",
                    "message": "This user has temporary restrictions on making new reservations. Please try again later.",
                }
            ),
            403,
        )
    # Verificamos si existe el vehiculo
    vehicle = mongo.db.vehiculos.find_one({"_id": vehicle_id})
    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404

    # Convertir las fechas de inicio y fin
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").replace(
            hour=0, minute=0, second=0
        )
        end_date = datetime.strptime(end_date, "%Y-%m-%d").replace(
            hour=0, minute=0, second=0
        )
    except ValueError as e:
        return jsonify({"error": "Invalid date format", "message": str(e)}), 400

    # Validar que la fecha de inicio sea en el futuro y que la fecha de fin sea posterior
    today_date = datetime.now().date()
    if start_date > end_date or start_date.date() < today_date:
        return (
            jsonify(
                {
                    "error": "Invalid dates. The start date must be in the future, and the end date must be later than the start date."
                }
            ),
            400,
        )

    # Verificar si ya existe una reserva activa para el vehículo en las fechas solicitadas
    reservation = check_reserve(vehicle_id, start_date, end_date)

    if reservation:
        response = {
            "message": "there are already active reservations for these dates",
            "reservation": reservation,
        }
        return Response(dumps(response), mimetype="application/json", status=400)

    # Defino el JSON para crear la reserva
    reservation = {
        "id_usuario": user_id,
        "id_vehiculo": vehicle_id,
        "fecha_inicio": start_date,
        "fecha_fin": end_date,
        "estado": "activa",
    }

    # Insertar la nueva reserva en la base de datos
    result = mongo.db.reservas.insert_one(reservation)
    reservation["_id"] = result.inserted_id

    # Actualizamos el historial de reservas
    update_historial(user_id, reservation["_id"], start_date)

    # Convertir la reserva a JSON y devolverla en la respuesta
    return Response(dumps(reservation), mimetype="application/json", status=201)


def cancel_reservation(id):
    try:
        id = ObjectId(id)
    except Exception as e:
        message = {"error": "Invalid ID", "message": str(e)}
        return jsonify(message), 400
    reservation = mongo.db.reservas.find_one({"_id": id})
    if reservation is None:
        return jsonify({"error": "Reservation not found"}), 404
    mongo.db.reservas.update_one({"_id": id}, {"$set": {"estado": "cancelado"}})

    # penalización para usuarios que cancelen +3 veces en una semana (ultimos 7 días)
    data = {
        "fecha": datetime.now(),
        "id_usuario": reservation["id_usuario"],
        "id_reserva": id,
    }
    mongo.db.cancelaciones.insert_one(data)

    seven_days_ago = datetime.now() - timedelta(days=7)
    count = mongo.db.cancelaciones.count_documents(
        {"id_usuario": reservation["id_usuario"], "fecha": {"$gte": seven_days_ago}}
    )

    # actualización del historial y estado del usuario
    mongo.db.usuarios.update_one(
        {"_id": reservation["id_usuario"], "historial_reservas.reserva_id": id},
        {"$set": {"historial_reservas.$.estado": "cancelado", "estado": count > 3}},
    )

    message = {"message": f"Reserva {id} cancelada"}
    return jsonify(message), 200


def activate_user(id):
    try:
        id = ObjectId(id)
    except Exception as e:
        message = {"error": "Invalid ID", "message": str(e)}
        return jsonify(message), 400
    user = mongo.db.usuarios.find_one({"_id": ObjectId(id)})
    if user is None:
        return jsonify({"error": "User not found"}), 404

    mongo.db.usuarios.update_one(
        {"_id": id},
        {"$set": {"estado": False}},
    )
    message = {"message": f"Usuario {id} activado"}
    return jsonify(message), 200


def get_reservations_by_user(id):
    try:
        id = ObjectId(id)
    except Exception as e:
        message = {"error": "Invalid ID", "message": str(e)}
        return jsonify(message), 400
    user = mongo.db.usuarios.find_one({"_id": ObjectId(id)})
    if user is None:
        return jsonify({"error": "User not found"}), 404
    reservations = mongo.db.reservas.find({"id_usuario": id})
    reservations = dumps(reservations)
    return Response(reservations, mimetype="application/json", status=200)


def get_most_reserved_vehicle():
    """
    Vehículo con la mayor cantidad de reservas.

    Returns:
        JSON: Información sobre el vehículo con más reservas.

    Raises:
        HTTPException:
            - 500: Si ocurre un error inesperado al obtener el vehículo más reservado.
    """
    pipeline = [
        {"$group": {"_id": "$id_vehiculo", "cantidad": {"$sum": 1}}},
        {"$sort": {"cantidad": -1}},
        {"$limit": 1},
    ]
    resultado = mongo.db.reservas.aggregate(pipeline)
    vehicle = list(resultado)
    if not vehicle:
        return jsonify({"error": "No reservations found"}), 404

    most_reserved_vehicle_id = vehicle[0]["_id"]
    vehicle_ = mongo.db.vehiculos.find_one({"_id": most_reserved_vehicle_id})
    if not vehicle_:
        return jsonify({"error": "Vehicle not found"}), 404

    response = {
        "id_vehiculo": most_reserved_vehicle_id,
        "cantidad_reservas": vehicle[0]["cantidad"],
        "vehiculo": vehicle_,
    }

    return Response(dumps(response), mimetype="application/json", status=200)


def get_most_canceling_user(limit=1):
    """
    Obtiene los usuarios que más han cancelado reservas.

    Args:
        limit (int): Número máximo de usuarios a devolver, por defecto 1.

    Returns:
        JSON: Usuarios con más cancelaciones.

    Raises:
        HTTPException:
            - 500: Si ocurre un error inesperado al obtener los usuarios que más cancelan.
    """
    try:
        if not isinstance(limit, int) or limit <= 0:
            return jsonify({"error": "'limit' must be a positive integer."}), 400

        pipeline = [
            {"$group": {"_id": "$id_usuario", "cantidad_cancelaciones": {"$sum": 1}}},
            {"$sort": {"cantidad_cancelaciones": -1}},
            {"$limit": limit},
        ]
        resultado = mongo.db.cancelaciones.aggregate(pipeline)
        users = list(resultado)

        if not users:
            return jsonify({"error": "No cancellations found"}), 404

        response = []
        for user in users:
            user_id = user["_id"]
            user_details = mongo.db.usuarios.find_one({"_id": user_id})

            if user_details:
                response.append(
                    {
                        "id_usuario": user_id,
                        "cantidad_cancelaciones": user["cantidad_cancelaciones"],
                        "usuario": user_details,
                    }
                )

        return Response(dumps(response), mimetype="application/json", status=200)

    except Exception as e:
        return jsonify({"error": "An error occurred", "message": str(e)}), 500
