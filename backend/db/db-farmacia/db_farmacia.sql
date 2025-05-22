DROP DATABASE IF EXISTS farmacias;
CREATE DATABASE farmacias
    WITH ENCODING 'UTF8'
         LC_COLLATE = 'en_US.utf8'
         LC_CTYPE  = 'en_US.utf8'
         TEMPLATE  = template0;

\connect farmacias;

CREATE TABLE farmacia (
    id_farmacia             SERIAL PRIMARY KEY,
    nombre_farmacia         VARCHAR(255) NOT NULL,
    direccion               VARCHAR(255) NOT NULL,
    comuna                  VARCHAR(255) NOT NULL
);