-- ============================================================
-- Script para PostgreSQL: Microservicio de Usuarios Farmacia
-- Actualizado para incluir stock y relación productos-farmacias
-- ============================================================

-- 1. Eliminar y crear la base de datos
DROP DATABASE IF EXISTS usuarios_farmacia;

CREATE DATABASE usuarios_farmacia
     WITH ENCODING 'UTF8'
          LC_COLLATE = 'en_US.utf8'
          LC_CTYPE  = 'en_US.utf8'
          TEMPLATE   = template0;

\connect usuarios_farmacia;

-- 2. Tabla de usuarios
CREATE TABLE usuarios (
    id_usuario      SERIAL PRIMARY KEY,
    rut             VARCHAR(12) UNIQUE NOT NULL,
    nombre          VARCHAR(100) NOT NULL,
    apellido        VARCHAR(100) NOT NULL,
    correo          VARCHAR(150) UNIQUE NOT NULL,
    contrasena      TEXT NOT NULL,
    telefono        VARCHAR(20),
    rol             VARCHAR(50) CHECK (rol IN ('cliente', 'admin', 'farmaceutico')) DEFAULT 'cliente',
    estado          BOOLEAN DEFAULT TRUE,
    fecha_registro  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    beneficiario    BOOLEAN DEFAULT FALSE,
    medicamentos    TEXT,
    retiro_en_dias  INTEGER  
);

