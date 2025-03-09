from config.config import app
from flasgger import Swagger
from crud.users import *
from flask import request

# inicializamos swagger
swagger = Swagger(app)


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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
