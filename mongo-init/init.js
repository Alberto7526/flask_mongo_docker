// creamos la base de datos y las colecciones necesarias

db = db.getSiblingDB('reservas_db');

// Crear colecciones 
db.createCollection("usuarios");
db.createCollection("vehiculos");
db.createCollection("reservas");
db.createCollection("cancelaciones");

// Insertar datos iniciales
db.usuarios.insertOne({
    "nombre": "Pepito Perez",
    "email": "pepito@example.com",
    "estado": false,
    "reservas": []
    
});

db.vehiculos.insertOne({
    "tipo": "sedan",
    "placa": "ABC123",
    "disponibilidad": true
});



