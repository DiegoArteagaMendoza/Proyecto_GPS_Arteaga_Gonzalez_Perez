-- 1. Eliminar y crear la base de datos si ya existe
DROP DATABASE IF EXISTS trabajadores;
CREATE DATABASE trabajadores
    WITH ENCODING 'UTF8'
         LC_COLLATE = 'en_US.utf8'
         LC_CTYPE  = 'en_US.utf8'
         TEMPLATE  = template0;

\connect trabajadores;

-- 3. Tabla: Rol
-- Define los distintos roles que puede tener un trabajador
CREATE TABLE rol (
    id_rol      SERIAL PRIMARY KEY,
    nombre_rol  VARCHAR(255) NOT NULL UNIQUE,
    descripcion TEXT
);

-- 4. Tabla: Trabajador
-- Información básica del trabajador
CREATE TABLE trabajador (
    id_trabajador     SERIAL PRIMARY KEY,
    nombre            VARCHAR(255) NOT NULL,
    apellido          VARCHAR(255) NOT NULL,
    rut               VARCHAR(20)  NOT NULL UNIQUE,
    fecha_nacimiento  DATE,
    direccion         TEXT,
    telefono          VARCHAR(20),
    correo_electronico VARCHAR(255),
    fecha_contratacion DATE DEFAULT CURRENT_DATE,
    estado            BOOLEAN DEFAULT TRUE,
    rol               VARCHAR(100) NOT NULL,
    contrasena        VARCHAR(255)
);