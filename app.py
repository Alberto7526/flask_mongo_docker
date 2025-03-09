from config.config import app
from flasgger import Swagger
from crud.users import *
from crud.vehicles import *
from flask import request

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
        200:
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
                    disponible:
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
            disponibliidad:
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
        200:
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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
