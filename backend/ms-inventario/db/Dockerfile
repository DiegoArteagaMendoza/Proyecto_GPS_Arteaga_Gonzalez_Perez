# Usar la imagen oficial de PostgreSQL
FROM postgres:13

# Variables de entorno (ajusta según tu configuración)
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=secret

# Copiar el archivo SQL al directorio de inicialización
COPY db_inventario.sql /docker-entrypoint-initdb.d/

# Puerto expuesto (opcional, ya que PostgreSQL lo expone por defecto)
EXPOSE 5432