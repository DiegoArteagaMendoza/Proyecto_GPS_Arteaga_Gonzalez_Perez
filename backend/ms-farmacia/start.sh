#!/bin/sh

# Si PORT no está definido, usa 8000 por defecto
PORT=${PORT:-8000}

# Inicia Gunicorn usando el puerto definido
exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT