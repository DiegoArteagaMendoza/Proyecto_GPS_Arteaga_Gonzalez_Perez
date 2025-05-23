
-- 1. Crear la base de datos
DROP DATABASE IF EXISTS venta;
CREATE DATABASE venta
     WITH ENCODING 'UTF8'
          LC_COLLATE = 'en_US.utf8'
          LC_CTYPE  = 'en_US.utf8'
          TEMPLATE   = template0;
\connect venta;

-- 2. Tablas base referenciadas
CREATE TABLE ventas (
    id_venta           SERIAL PRIMARY KEY,
    fecha_venta        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rut_cliente        VARCHAR(20) NOT NULL, -- Si deseas saber quién realizó la compra (cliente)
    total_venta        DECIMAL(12,2) NOT NULL,
    metodo_pago        VARCHAR(50) NOT NULL, -- efectivo, débito, crédito, etc.
    estado_venta       VARCHAR(20) DEFAULT 'completada', -- 'pendiente', 'anulada'
    farmacia           VARCHAR(255) NOT NULL
);

CREATE TABLE detalle_venta (
    id_detalle         SERIAL PRIMARY KEY,
    id_venta           INTEGER NOT NULL REFERENCES ventas(id_venta),
    id_producto        INTEGER NOT NULL, -- Para trazabilidad, puedes guardar el id del producto
    nombre_producto    VARCHAR(255),
    cantidad           DECIMAL(10,2),
    precio_unitario    DECIMAL(12,2),
    subtotal           DECIMAL(12,2) -- cantidad * precio_unitario
);

CREATE TABLE boletas (
    id_boleta          SERIAL PRIMARY KEY,
    id_venta           INTEGER NOT NULL REFERENCES ventas(id_venta),
    numero_boleta      VARCHAR(100),
    tipo_documento     VARCHAR(50) DEFAULT 'boleta', -- boleta, factura, nota_credito
    fecha_emision      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total              DECIMAL(12,2),
    rut_cliente        VARCHAR(20), -- Opcional, para facturas
    nombre_cliente     VARCHAR(255)
);
