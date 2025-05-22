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
    contraseña      TEXT NOT NULL,
    telefono        VARCHAR(20),
    rol             VARCHAR(50) CHECK (rol IN ('cliente', 'admin', 'farmaceutico')) DEFAULT 'cliente',
    estado          BOOLEAN DEFAULT TRUE,
    fecha_registro  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabla de farmacias
CREATE TABLE farmacias (
    id_farmacia     SERIAL PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    direccion       TEXT NOT NULL,
    telefono        VARCHAR(20),
    correo          VARCHAR(150) UNIQUE NOT NULL,
    estado          BOOLEAN DEFAULT TRUE,
    fecha_registro  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Relación entre usuarios y farmacias (muchos a muchos)
CREATE TABLE usuarios_farmacia (
    id_usuario_farmacia SERIAL PRIMARY KEY,
    id_usuario          INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    id_farmacia         INTEGER NOT NULL REFERENCES farmacias(id_farmacia),
    fecha_asignacion    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (id_usuario, id_farmacia)
);

-- 5. Tabla de productos básicos (solo para esta BD)
CREATE TABLE productos (
    id_producto    SERIAL PRIMARY KEY,
    nombre         VARCHAR(255) NOT NULL,
    descripcion    TEXT
);

-- 6. Relación productos-farmacias (muchos a muchos + stock)
CREATE TABLE productos_farmacia (
    id_producto_farmacia SERIAL PRIMARY KEY,
    id_producto          INTEGER NOT NULL REFERENCES productos(id_producto),
    id_farmacia          INTEGER NOT NULL REFERENCES farmacias(id_farmacia),
    stock                INTEGER NOT NULL CHECK (stock >= 0),
    disponible           BOOLEAN DEFAULT TRUE,
    fecha_actualizacion  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (id_producto, id_farmacia)
);

-- 7. Medicamentos asignados a clientes (usuario con producto)
CREATE TABLE medicamentos_cliente (
    id_medicamento_cliente SERIAL PRIMARY KEY,
    id_usuario_cliente     INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    id_producto            INTEGER NOT NULL REFERENCES productos(id_producto),
    fecha_asignacion       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    retiro                 BOOLEAN DEFAULT FALSE,
    fecha_retiro           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (id_usuario_cliente, id_producto)
);

-- Insertar farmacias de ejemplo
INSERT INTO farmacias (nombre, direccion, telefono, correo) VALUES
('Farmacia Central', 'Av. Libertador 1234, Santiago', '22223333', 'central@farmacia.cl'),
('Farmacia Norte', 'Calle Norte 456, Antofagasta', '22557788', 'norte@farmacia.cl'),
('Farmacia Sur', 'Av. Sur 789, Concepción', '22334455', 'sur@farmacia.cl');

-- Insertar productos comunes en farmacias
INSERT INTO productos (nombre, descripcion) VALUES
('Paracetamol 500mg', 'Analgésico y antipirético de uso general'),
('Ibuprofeno 400mg', 'Antiinflamatorio no esteroide (AINE) para dolor e inflamación'),
('Amoxicilina 500mg', 'Antibiótico de amplio espectro para infecciones bacterianas'),
('Loratadina 10mg', 'Antihistamínico para alergias y rinitis'),
('Omeprazol 20mg', 'Inhibidor de la bomba de protones para tratamiento de gastritis y reflujo'),
('Salbutamol Inhalador', 'Broncodilatador de acción rápida para asma'),
('Metformina 850mg', 'Fármaco oral para la diabetes tipo 2'),
('Losartán 50mg', 'Antihipertensivo usado en el tratamiento de la presión arterial alta'),
('Simvastatina 20mg', 'Reductor de colesterol para prevención cardiovascular'),
('Vitamina C 1g', 'Suplemento vitamínico antioxidante para fortalecer el sistema inmune');

-- Insertar disponibilidad de productos en farmacias con stock
INSERT INTO productos_farmacia (id_producto, id_farmacia, stock) VALUES
(1, 1, 100),  -- Paracetamol en Farmacia Central
(1, 2, 50),   -- Paracetamol en Farmacia Norte
(2, 1, 80),   -- Ibuprofeno en Central
(3, 3, 60),   -- Amoxicilina en Sur
(4, 1, 30),   -- Loratadina en Central
(4, 3, 40),   -- Loratadina en Sur
(5, 2, 20),   -- Omeprazol en Norte
(6, 1, 15),   -- Salbutamol en Central
(7, 2, 45),   -- Metformina en Norte
(8, 3, 35),   -- Losartán en Sur
(9, 1, 50),   -- Simvastatina en Central
(10, 2, 100); -- Vitamina C en Norte
