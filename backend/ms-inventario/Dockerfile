# FROM python:3.9.13-slim
# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY src/ .

# # EXPOSE 8000
# CMD ["sh", "-c", "gunicorn core.wsgi:application --bind 0.0.0.0:$PORT"]
# # CMD ["gunicorn","core.wsgi:application","--bind","0.0.0.0:$PORT"]

FROM python:3.9.13-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

# Copia el script de inicio
COPY start.sh /start.sh

# Damos permiso de ejecución
RUN chmod +x /start.sh

EXPOSE 8081

# Usamos el script como punto de entrada
CMD ["/start.sh"]