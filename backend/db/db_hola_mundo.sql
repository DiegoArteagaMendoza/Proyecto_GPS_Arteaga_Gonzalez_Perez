-- Crear la base de datos (aunque POSTGRES_DB ya la crea, esto es opcional si quieres forzarlo)
 CREATE DATABASE holamundo;
 
 -- Conectarse a la base de datos creada
 \connect holamundo;
 
 -- Crear la tabla 'prueba'
 CREATE TABLE prueba (
     id SERIAL PRIMARY KEY,
     titulo VARCHAR(255),
     telefono VARCHAR(20),
     estado VARCHAR(50)
 );