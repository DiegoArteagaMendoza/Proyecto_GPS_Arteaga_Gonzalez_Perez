-- ====================================================
-- Script completo para PostgreSQL: Base de datos "inventario"
-- Incluye:
--   • Creación de la base de datos
--   • Tablas: productos, bodegas, inventario, movimientos_inventario
--   • Función y triggers para mantener stock actualizado
-- ====================================================

-- 1. Crear la base de datos
DROP DATABASE IF EXISTS inventario;
CREATE DATABASE inventario
     WITH ENCODING 'UTF8'
          LC_COLLATE = 'en_US.utf8'
          LC_CTYPE  = 'en_US.utf8'
          TEMPLATE   = template0;
\connect inventario;

-- 2. Tablas base referenciadas

CREATE TABLE productos (
    id_producto    SERIAL PRIMARY KEY,
    nombre         VARCHAR(255) NOT NULL,
    descripcion    TEXT
);

CREATE TABLE bodegas (
    id_bodega      SERIAL PRIMARY KEY,
    nombre         VARCHAR(255) NOT NULL,
    ubicacion      TEXT
);

-- 3. Tabla principal de inventario

CREATE TABLE inventario (
    id_inventario        SERIAL PRIMARY KEY,
    id_producto          INTEGER NOT NULL REFERENCES productos(id_producto),
    nombre_producto      VARCHAR(255),
    id_bodega            INTEGER NOT NULL REFERENCES bodegas(id_bodega),
    lote                 VARCHAR(100),
    fecha_lote           DATE,
    fecha_vencimiento    DATE,
    cantidad             DECIMAL(10,2)   DEFAULT 0,
    unidad_medida        VARCHAR(50),
    costo_unitario       DECIMAL(12,4)   DEFAULT 0.0000,
    costo_promedio       DECIMAL(12,4)   DEFAULT 0.0000,
    precio_venta         DECIMAL(12,4)   DEFAULT 0.0000,
    stock_minimo         DECIMAL(10,2)   DEFAULT 0
);

-- 4. Tabla de movimientos de inventario (histórico)

CREATE TABLE movimientos_inventario (
    id_movimiento     SERIAL PRIMARY KEY,
    id_inventario     INTEGER NOT NULL REFERENCES inventario(id_inventario),
    tipo_movimiento   VARCHAR(20) CHECK (tipo_movimiento IN ('entrada','salida')),
    cantidad          DECIMAL(10,2) NOT NULL,
    fecha_movimiento  TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    observacion       TEXT,
    usuario           VARCHAR(100)
);