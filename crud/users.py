from config.config import mongo
from bson.json_util import dumps
from bson import ObjectId
from flask import Response, jsonify
import re

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


def get_users():
    """
    Obtiene todos los usuarios de la base de datos.

    Returns:
        list[users]: Una lista de todos los usuarios registrados.

    Raises:
        HTTPException:
            - 500: Si ocurre un error inesperado al obtener los usuarios.
    """
    users = mongo.db.usuarios.find()
    users = dumps(users)
    return Response(users, mimetype="application/json", status=200)


def get_user_by_id(id):
    """
    Obtiene un usuario por su ID

    Args:
        id (str): ID del usuario a buscar.

    returns:
        user: El objeto del usuario correspondiente al ID.

    Raises:
        HTTPException:
            - 404: Si el usuario no se encuentra en la base de datos.

    """
    try:
        id = ObjectId(id)
    except Exception as e:
        message = {"error": "Invalid ID", "message": str(e)}
        return jsonify(message), 400
    user = mongo.db.usuarios.find_one({"_id": ObjectId(id)})
    if user is None:
        return jsonify({"error": "User not found"}), 404
    user = dumps(user)
    return Response(user, mimetype="application/json", status=200)


def create_user(user):
    """
    Crea un nuevo usuario en la base de datos.

    Args:
        user (dict): Un diccionario con los datos del usuario a crear, debe incluir nombre, email.

    returns:
        id: El _id del objeto del usuario creado.

    Raises:
        HTTPException:
            - 400: Si faltan campos requeridos, si el email es inválido o si el email ya existe.
    """
    name = user.get("nombre")
    email = user.get("email")
    if name is None or email is None:
        return (
            jsonify(
                {
                    "error": "Missing required fields, please ensure your data includes 'nombre' and 'email'"
                }
            ),
            400,
        )
    if re.match(EMAIL_REGEX, email) is None:
        return jsonify({"error": "Invalid email"}), 400
    if mongo.db.usuarios.find_one({"email": email}):
        return jsonify({"error": "Email already exists"}), 400
    user = {"nombre": name, "email": email, "estado": False, "historial_reservas": []}
    user_id = mongo.db.usuarios.insert_one(user)
    return jsonify({"id": str(user_id.inserted_id)}), 201


def update_user(id, user):
    """
    Actualiza un usuario en la base de datos.

    Args:
        id (str): ID del usuario a actualizar.
        user (dict): Un diccionario con los datos del usuario a actualizar, debe incluir nombre, email.

    returns:
        id: El _id del objeto del usuario actualizado.

    Raises:
        HTTPException:
            - 400: Si el ID es inválido, si faltan campos requeridos, si el email es inválido o si el email ya existe.
    """
    try:
        id = ObjectId(id)
    except Exception as e:
        message = {"error": "Invalid ID", "message": str(e)}
        return jsonify(message), 400
    name = user.get("nombre")
    email = user.get("email")
    if name is None or email is None:
        return (
            jsonify(
                {
                    "error": "Missing required fields, please ensure your data includes 'nombre' and 'email'"
                }
            ),
            400,
        )
    if re.match(EMAIL_REGEX, email) is None:
        return jsonify({"error": "Invalid email"}), 400
    if mongo.db.usuarios.find_one(
        {"$and": [{"email": email}, {"_id": {"$ne": ObjectId(id)}}]}
    ):
        return jsonify({"error": "Email already exists"}), 400
    user = {"nombre": name, "email": email, "historial_reservas": []}
    mongo.db.usuarios.update_one({"_id": ObjectId(id)}, {"$set": user})
    return jsonify({"id": str(id)}), 200


def delete_user(id):
    """
    Elimina un usuario de la base de datos.

    Args:
        id (str): ID del usuario a eliminar.

    Returns:
        id: El _id del objeto del usuario eliminado.

    Raises:
        HTTPException:
            - 400: Si el ID es inválido.
            - 404: Si el usuario no se encuentra en la base de datos.
    """
    try:
        id = ObjectId(id)
    except Exception as e:
        message = {"error": "Invalid ID", "message": str(e)}
        return jsonify(message), 400
    user = mongo.db.usuarios.find_one({"_id": ObjectId(id)})
    if user is None:
        return jsonify({"error": "User not found"}), 404
    mongo.db.usuarios.delete_one({"_id": ObjectId(id)})
    return jsonify({"id": str(id)}), 200
