from config.config import mongo


def check_reserve(vehicle_id, start_date, end_date):
    """
    Realiza una consulta a la base de datos para verificar si existen reservas activas que se superpongan con las fechas entregadas

    Args:
        vehicle_id: Id del vehiculo
        start_date: Fecha inicial
        end_date: Fecha final
    returns:
        list(reservation): Una lista con todas las reservas que cumplan la coincidencia

    """
    reservation = list(
        mongo.db.reservas.find(
            {
                "$and": [
                    {"id_vehiculo": vehicle_id},
                    {"estado": "activa"},
                    {
                        "$or": [
                            {
                                "fecha_fin": {"$gte": start_date},
                                "fecha_inicio": {"$lte": end_date},
                            },
                            {
                                "fecha_inicio": {"$lte": end_date},
                                "fecha_fin": {"$gte": start_date},
                            },
                        ]
                    },
                ]
            }
        )
    )
    return reservation


def update_historial(user_id, reserva_id, start_date):
    """
    Actualiza el historial de reservas en el usuario asignado

    Args:
        user_id: Id del usuario
        reserva_id: Id de la reserva
        start_date: Fecha inicial
    """
    historial_reservas = {
        "reserva_id": reserva_id,
        "fecha": start_date,
        "estado": "confirmada",
    }

    mongo.db.usuarios.update_one(
        {"_id": user_id}, {"$push": {"historial_reservas": historial_reservas}}
    )
