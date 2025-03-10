# Reservas API

API REST para gestionar las reservas de vehículos, desarrollada con **Flask** y **MongoDB**.

## Características

- Permite **crear, leer, actualizar y eliminar** usuarios, vehículos.
  -Permite gestionar reservas
- **Consultar el historial de reservas** de los usuarios.
- **Documentación automática** con Swagger.
- **Pruebas automatizadas** con Pytest.
- **Contenerización con Docker**.

## Tecnologías Utilizadas

- **Flask** - Framework principal.
- **MongoDB** - Base de datos.
- **PyMongo** - Conector para MongoDB.
- **Flasgger** - Para generar la documentación de la API con Swagger.
- **Pytest** - Pruebas unitarias e integración.
- **Docker** - Contenerización de la aplicación.

## Instalación y Ejecución

### 1. Clonar el Repositorio

```sh
git clone https://github.com/Alberto7526/flask_mongo_docker.git
cd flask_mongo_docker
```

### 2. Construir y Levantar los Contenedores

```sh
docker-compose up -d
```

Esto iniciará la API y MongoDB en contenedores.

### 3. Acceder a la API

- **Swagger UI**: [http://localhost:5000/apidocs](http://localhost:5000/apidocs)

## Endpoints Principales

### Usuarios

| Método | Endpoint      | Descripción                |
| ------ | ------------- | -------------------------- |
| POST   | `/users/`     | Crear un usuario           |
| GET    | `/users/`     | Obtener todos los usuarios |
| GET    | `/users/{id}` | Obtener un usuario por ID  |
| PUT    | `/users/{id}` | Actualizar un usuario      |
| DELETE | `/users/{id}` | Eliminar un usuario        |

### Vehículos

| Método | Endpoint         | Descripción                 |
| ------ | ---------------- | --------------------------- |
| POST   | `/vehicles/`     | Crear un vehículo           |
| GET    | `/vehicles/`     | Obtener todos los vehículos |
| GET    | `/vehicles/{id}` | Obtener un vehículo por ID  |
| PUT    | `/vehicles/{id}` | Actualizar un vehículo      |
| DELETE | `/vehicles/{id}` | Eliminar un vehículo        |

### Reservas

| Método | Endpoint                 | Descripción                              |
| ------ | ------------------------ | ---------------------------------------- |
| POST   | `/reserve/`              | Crear una reserva                        |
| GET    | `/reserve/`              | Obtener todas las reservas               |
| PUT    | `/reserve/{id}`          | Cancelar una reserva                     |
| GET    | `/reserve/user/{id}`     | Obtener todas las reservas de un usuario |
| PUT    | `/reserve/user/{id}`     | Activa el usuario bloqueado              |
| GET    | `/reserve/vehicle/`      | Obtener el vehículo más reservado        |
| GET    | `/reserve/users/{limit}` | Usuarios con más cancelaciones           |

## Ejecutar Pruebas

Para ejecutar las pruebas dentro del contenedor:

```sh
docker-compose exec api bash -c "export PYTHONPATH=/app && pytest --import-mode=importlib"
```

## Esquema de la base de datos mongoDB

La base de datos está compuesta por las siguientes colecciones: **usuarios**, **vehículos**, **reservas**, y **cancelaciones**. A continuación se detallan cada uno de ellos

### 1. **Usuarios**

La colección **usuarios** almacena la información de los usuarios que pueden realizar reservas.

#### Esquema:

```json
{
  "_id": ObjectId("..."),
  "nombre": "String",            // Nombre del usuario
  "email": "String",             // Correo electrónico del usuario (único)
  "estado": "Boolean",           // Estado del usuario (Para penalización)
  "reservas": [ObjectId]         // Lista de las reservas realizadas por el usuario
}
```

---

### 2. **Vehículos**

La colección **vehículos** almacena los datos relacionados con los vehículos disponibles para ser reservados.

#### Esquema:

```json
{
  "_id": ObjectId("..."),
  "tipo": "String",              // Tipo de vehículo (sedan, SUV, etc.)
  "placa": "String",             // Placa del vehículo (unico)
  "disponibilidad": "Boolean"    // Disponibilidad del vehículo para ser reservado
}
```

---

### 3. **Reservas**

La colección **reservas** almacena las reservas realizadas por los usuarios.

#### Esquema:

```json
{
  "_id": ObjectId("..."),
  "id_usuario": ObjectId,        // ID del usuario que realizó la reserva
  "id_vehiculo": ObjectId,       // ID del vehículo reservado
  "fecha_inicio": "Date",       // Fecha y hora de inicio de la reserva
  "fecha_fin": "Date",       // Fecha y hora de finalización de la reserva
  "estado": "String"             // Estado de la reserva (confirmada, terminado, cancelado)
}
```

---

### 4. **Cancelaciones**

La colección **cancelaciones** almacena información sobre las reservas canceladas para penalización de usuarios por más de 3 cancelaciones en los ultimos 7 días.

#### Esquema:

```json
{
  "_id": ObjectId("..."),
  "fecha": "Date",    // Fecha y hora de la cancelación
  "id_reserva": ObjectId,         // ID de la reserva cancelada
  "id_usuario": ObjectId,         // ID del usuario de la reserva
}
```

---

## Lógica para la penalización de usuarios que tienen más de 3 cancelaciones en los ultimos 7 días

Se creó la colección _cancelaciones_, la cual es alimentada cada vez que se realiza una cancelación, al mismo tiempo se valida la cantidad de cancelaciones por usuario y se cambia el estado en la colección de usuarios a **true** por defecto **false** cuando este tiene más de 3 cancelaciones.

Cuando un usuario va a realizar una reserva se valdia este dato y si es verdadero devolvera un mensaje como este:

```json
{
  "error": "User temporarily blocked from making reservations.",
  "message": "This user has temporary restrictions on making new reservations. Please try again later."
}
```

Para habilitarlo nuevamente se debe usar el siguiente endpoint

```
 PUT    | `/reserve/user/{id}`     | Activa el usuario bloqueado
```
