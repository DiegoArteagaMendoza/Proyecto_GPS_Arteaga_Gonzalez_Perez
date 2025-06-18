#!/bin/sh

# Usamos el valor de PORT, o 8000 como fallback
PORT=${PORT:-8080}

echo "Iniciando Gunicorn en puerto $PORT"
exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT