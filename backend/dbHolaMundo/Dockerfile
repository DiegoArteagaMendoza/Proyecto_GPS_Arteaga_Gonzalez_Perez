# Usa la imagen oficial de PostgreSQL como base
FROM postgres:13

# Establece variables de entorno para PostgreSQL
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=secret

# Copia el archivo SQL al directorio /docker-entrypoint-initdb.d/
# Los archivos en este directorio se ejecutan automáticamente durante la inicialización de PostgreSQL
COPY db_hola_mundo.sql /docker-entrypoint-initdb.d/

# Indica que el contenedor debe exponer el puerto 5432 (puerto predeterminado de PostgreSQL)
EXPOSE 5432

# Comando predeterminado para iniciar PostgreSQL
CMD ["postgres"]