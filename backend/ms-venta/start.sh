#!/bin/sh

PORT=${PORT:-8084}

echo "Creando migraciones..."
python manage.py makemigrations

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Iniciando Gunicorn en puerto $PORT"
exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
