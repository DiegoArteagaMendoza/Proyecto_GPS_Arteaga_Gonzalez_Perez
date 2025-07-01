# Usa una imagen base ligera de Nginx
FROM nginx:alpine

# Elimina el contenido por defecto del directorio HTML de Nginx
RUN rm -rf /usr/share/nginx/html/*

# Copia los archivos HTML al directorio raíz
COPY src/html/ /usr/share/nginx/html/

# Copia los archivos CSS a una carpeta css/
COPY src/css/ /usr/share/nginx/html/css/

# Copia los archivos JS a una carpeta js/
COPY src/js/ /usr/share/nginx/html/js/

# Expone el puerto 80 (requerido por Railway)
EXPOSE 80

# No es necesario sobrescribir el CMD, Nginx ya se inicia por defecto
