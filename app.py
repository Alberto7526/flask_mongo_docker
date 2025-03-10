from flask import Flask, request
from flask_pymongo import PyMongo
from flasgger import Swagger

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/reservas_db"
mongo = PyMongo(app)

from crud.users import *
from crud.vehicles import *
from crud.reserves import *


# inicializamos swagger

swagger = Swagger(
    app,
    template={
        "info": {
            "title": "API Reservas",
            "description": "API para el manejo de reservas de vehículos",
            "version": "1.0.0",
        }
    },
)


# Rutas usuarios


@app.route("/users", methods=["GET"])
def get_users_endpoint():
    """
    Listar todos los usuarios
    ---
    description: Obtiene todos los usuarios de la base de datos.
    responses:
      200:
        description: Lista de usuarios
        schema:
          type: array
          items:
            type: object
            properties:
              _id:
                type: string
                description: ID del usuario
              nombre:
                type: string
                description: Nombre del usuario
              email:
                type: string
                description: Correo electrónico del usuario
              historial_reservas:
                type: array
                description: Historial de reservas del usuario
                items:
                  type: object
                  properties:
                    reserva_id:
                      type: string
                      description: ID de la reserva
                    fecha:
                      type: string
                      description: Fecha de la reserva
                      example: "2025-03-09T15:00:00"
                    estado:
                      type: string
                      description: Estado de la reserva
                      example: "confirmada"
    """
    return get_users()


@app.route("/users/<id>", methods=["GET"])
def get_user_by_id_endpoint(id):
    """
    Buscar un usuario por su ID
    ---
    description: Obtiene un usuario por su ID
    parameters:
      - name: id
        in: path
        description: ID del usuario a buscar
        required: true
        type: string
    responses:
        200:
            description: Usuario encontrado
            schema:
                type: object
                properties:
                    _id:
                        type: string
                        description: ID del usuario
                    nombre:
                        type: string
                        description: Nombre del usuario
                    email:
                        type: string
                        description: Correo electrónico del usuario
                    historial_reservas:
                        type: array
                        description: Historial de reservas del usuario
                        items:
                            type: object
                            properties:
                                reserva_id:
                                    type: string
                                    description: ID de la reserva
                                fecha:
                                    type: string
                                    description: Fecha de la reserva
                                    example: "2025-03-09T15:00:00"
                                estado:
                                    type: string
                                    description: Estado de la reserva
                                    example: "confirmada"
        404:
            description: Usuario no encontrado
        400:
            description: ID inválido
    """
    return get_user_by_id(id)


@app.route("/users", methods=["POST"])
def create_user_endpoint():
    """
    Crear un usuario
    ---
    description: Crea un nuevo usuario en la base de datos.
    parameters:
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              description: Nombre del usuario
            email:
              type: string
              description: Correo electrónico del usuario
    responses:
        201:
            description: Id usuario creado
            schema:
                type: string
                description: ID del usuario creado
        400:
            description: Campos requeridos faltantes, email inválido o email ya existente
    """
    user = request.json
    return create_user(user)


@app.route("/users/<id>", methods=["PUT"])
def update_user_endpoint(id):
    """
    Actualiza un usuario
    ---
    description: Actualiza un usuario en la base de datos.
    parameters:
      - name: id
        in: path
        description: ID del usuario a actualizar
        required: true
        type: string
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              description: Nombre del usuario
            email:
              type: string
              description: Correo electrónico del usuario
    responses:
        200:
            description: Id usuario actualizado
            schema:
                type: string
                description: ID del usuario actualizado
        400:
            description: ID inválido, campos requeridos faltantes, email inválido o email ya existente
    """
    user = request.json
    return update_user(id, user)


@app.route("/users/<id>", methods=["DELETE"])
def delete_user_endpoint(id):
    """
    Elimina un usuario
    ---
    description: Elimina un usuario de la base de datos.
    parameters:
      - name: id
        in: path
        description: ID del usuario a eliminar
        required: true
        type: string
    responses:
        204:
            description: Id usuario eliminado
            schema:
                type: string
                description: ID del usuario eliminado
        400:
            description: ID inválido
        404:
            description: Usuario no encontrado
    """
    return delete_user(id)


# rutas de vehiculos
@app.route("/vehicles", methods=["GET"])
def get_vehicles_endpoint():
    """
    Listar todos los vehículos
    ---
    description: Obtiene todos los vehículos de la base de datos.
    responses:
      200:
        description: Lista de vehículos
        schema:
          type: array
          items:
            type: object
            properties:
              _id:
                type: string
                description: ID del vehículo
              placa:
                type: string
                description: Placa del vehículo
              disponible:
                type: boolean
                description: Estado de reserva del vehículo
    """
    return get_vehicles()


@app.route("/vehicles/<id>", methods=["GET"])
def get_vehicle_by_id_endpoint(id):
    """
    Buscar un vehículo por su ID
    ---
    description: Obtiene un vehículo por su ID
    parameters:
      - name: id
        in: path
        description: ID del vehículo a buscar
        required: true
        type: string
    responses:
        200:
            description: Vehículo encontrado
            schema:
                type: object
                properties:
                    _id:
                        type: string
                        description: ID del vehículo
                    tipo:
                        type: string
                        description: Tipo de vehículo
                    placa:
                        type: string
                        description: Placa del vehículo
                    disponibilidad:
                        type: boolean
                        description: Estado de reserva del vehículo
        404:
            description: Vehículo no encontrado
        400:
            description: ID inválido
    """
    return get_vehicle_by_id(id)


@app.route("/vehicles", methods=["POST"])
def create_vehicle_endpoint():
    """
    Crear un vehículo
    ---
    description: Crea un nuevo vehículo en la base de datos.
    parameters:
      - name: vehicle
        in: body
        required: true
        schema:
          type: object
          properties:
            tipo:
              type: string
              description: Tipo de vehículo
            placa:
              type: string
              description: Placa del vehículo
    responses:
        201:
            description: Id vehículo creado
            schema:
                type: string
                description: ID del vehículo creado
        400:
            description: Campos requeridos faltantes o vehículo ya existente
    """
    vehicle = request.json
    return create_vehicle(vehicle)


@app.route("/vehicles/<id>", methods=["PUT"])
def update_vehicle_endpoint(id):
    """
    Actualiza un vehículo
    ---
    description: Actualiza un vehículo en la base de datos.
    parameters:
      - name: id
        in: path
        description: ID del vehículo a actualizar
        required: true
        type: string
      - name: vehicle
        in: body
        required: true
        schema:
          type: object
          properties:
            tipo:
              type: string
              description: Tipo de vehículo
            placa:
              type: string
              description: Placa del vehículo
            disponibilidad:
              type: boolean
              description: Estado del vehículo
    responses:
        200:
            description: Id vehículo actualizado
            schema:
                type: string
                description: ID del vehículo actualizado
        400:
            description: ID inválido, campos requeridos faltantes o placa ya existente
        404:
            description: Vehículo no encontrado
        500:
            description: Error inesperado al actualizar el vehículo
    """
    vehicle = request.json
    return update_vehicle(id, vehicle)


@app.route("/vehicles/<id>", methods=["DELETE"])
def delete_vehicle_endpoint(id):
    """
    Elimina un vehículo
    ---
    description: Elimina un vehículo de la base de datos.
    parameters:
      - name: id
        in: path
        description: ID del vehículo a eliminar
        required: true
        type: string
    responses:
        204:
            description: Id vehículo eliminado
            schema:
                type: string
                description: ID del vehículo eliminado
        400:
            description: ID inválido
        404:
            description: Vehículo no encontrado
    """
    return delete_vehicle(id)


# Rutas reservas


@app.route("/reserve", methods=["GET"])
def get_reserves_endpoint():
    """
    Listar todas las reservas
    ---
    description: Obtiene todas las reservas de la base de datos.
    responses:
      200:
        description: Lista de reservas
        schema:
          type: array
          items:
            type: object
            properties:
              _id:
                type: string
                description: ID de la reserva
              id_usuario:
                type: string
                description: Id del usuario
              id_vehiculo:
                type: string
                description: Id del vehiculo
              fecha_inicio:
                type: string
                format: date
                description: Fecha y hora de inicio de la reserva (formato YYYY-MM-DD)
              fecha_fin:
                type: string
                format: date
                description: Fecha y hora de inicio de la reserva (formato YYYY-MM-DD)
    """
    return get_reserves()


@app.route("/reserve", methods=["POST"])
def create_reservation_endpoint():
    """
    Crear una reserva
    ---
    description: Crea una nueva reserva en la base de datos
    parameters:
      - name: reservation
        in: body
        required: true
        schema:
          type: object
          properties:
            id_usuario:
              type: string
              description: Id del usuario
            id_vehiculo:
              type: string
              description: Id del vehiculo
            fecha_inicio:
              type: string
              format: date
              description: Fecha y hora de inicio de la reserva (formato YYYY-MM-DD)
            fecha_fin:
              type: string
              format: date
              description: Fecha y hora de inicio de la reserva (formato YYYY-MM-DD)
    responses:
      201:
          description: Id de la reserva creada
          schema:
              type: string
              description: ID del vehículo creado
      400:
          description: Campos requeridos faltantes o vehículo ya existente
    """
    reservation = request.json
    return create_reservation(reservation)


@app.route("/reserve/<id>", methods=["PUT"])
def cancel_reservation_endpoint(id):
    """
    Cancelar reservas
    ---
    description: Actualiza una reserva a estado cancelado
    parameters:
      - name: id
        in: path
        description: ID de la reserva a cancelar
        required: true
        type: string
    responses:
        200:
            description: mensaje con el id de la reserva actualizada
            schema:
                type: string
                description: ID de la reserva cancelada
        400:
            description: ID inválido

    """
    return cancel_reservation(id)


@app.route("/reserve/user/<id>", methods=["PUT"])
def activate_user_endpoint(id):
    """
    Activar usuario para reservas
    ---
    description: Actualiza un usuario para que nuevamente pueda hacer reservas
    parameters:
      - name: id
        in: path
        description: ID del usuario
        required: true
        type: string
    responses:
        200:
            description: mensaje con el id del usuario activado
            schema:
                type: string
                description: ID del usuario
        400:
            description: ID inválido
        404:
            description: Usuario no encontrado
    """
    return activate_user(id)


@app.route("/reserve/user/<id>", methods=["GET"])
def get_reservations_by_user_endpoint(id):
    """
    Listar todas las reservas por usuario
    ---
    description: Obtiene todas las reservas de la base de datos por usuario.
    parameters:
        - name: id
          in: path
          description: ID del usuario a consultar
          required: true
          type: string
    responses:
      200:
        description: Lista de reservas
        schema:
          type: array
          items:
            type: object
            properties:
              _id:
                type: string
                description: ID de la reserva
              id_usuario:
                type: string
                description: Id del usuario
              id_vehiculo:
                type: string
                description: Id del vehiculo
              fecha_inicio:
                type: string
                format: date
                description: Fecha y hora de inicio de la reserva (formato YYYY-MM-DD)
              fecha_fin:
                type: string
                format: date
                description: Fecha y hora de inicio de la reserva (formato YYYY-MM-DD)
    """
    return get_reservations_by_user(id)


@app.route("/reserve/vehicle/", methods=["GET"])
def get_most_reserved_vehicle_endpoint():
    """
    Vehiculo más reservado
      ---
      description: Obtiene el vehiculo más reservado
      parameters:
        - name: limit
          in: path
          description: Limite de resultados
          required: true
          type: string
      responses:
        200:
            description: Vehículo más reservado
            schema:
                type: object
                properties:
                    _id:
                        type: string
                        description: ID del vehículo
                    tipo:
                        type: string
                        description: Tipo de vehículo
                    placa:
                        type: string
                        description: Placa del vehículo
                    disponibilidad:
                        type: boolean
                        description: Estado de reserva del vehículo
        404:
            description: Vehículo no encontrado
        400:
            description: ID inválido
    """
    return get_most_reserved_vehicle()


@app.route("/reserve/users/<int:limit>", methods=["GET"])
def get_most_canceling_user_limit(limit):
    """
    Usuarios con más cancelaciones
      ---
      description: Obtiene los usuarios que más han cancelado reservas
      parameters:
        - name: limit
          in: path
          description: Límite de resultados
          required: true
          type: integer
      responses:
        200:
            description: Usuarios con más cancelaciones
            schema:
                type: array
                items:
                    type: object
                    properties:
                        id_usuario:
                            type: string
                            description: ID del usuario
                        cantidad_cancelaciones:
                            type: integer
                            description: Cantidad de cancelaciones realizadas por el usuario
                        usuario:
                            type: object
                            properties:
                                nombre:
                                    type: string
                                    description: Nombre del usuario
                                email:
                                    type: string
                                    description: Correo del usuario
        404:
            description: No se encontraron cancelaciones
        400:
            description: Límite inválido
    """
    return get_most_canceling_user(
        limit
    )  # Pasar el 'limit' a la función de obtener el usuario que más ha cancelado


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
