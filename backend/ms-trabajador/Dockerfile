FROM python:3.9.13-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 8000
CMD ["sh", "-c", "gunicorn core.wsgi:application --bind 0.0.0.0:$PORT"]
# CMD ["gunicorn","core.wsgi:application","--bind","0.0.0.0:$PORT"]