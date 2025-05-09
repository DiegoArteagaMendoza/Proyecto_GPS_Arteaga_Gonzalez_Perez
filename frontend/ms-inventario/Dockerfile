# Etapa 1: Construcción del código Angular
FROM node:18-alpine AS build
WORKDIR /app
COPY package.json . /app/
RUN npm install
COPY . /app
RUN npm run build --prod

# Etapa 2: Servir la app con nginx
FROM nginx:alpine

COPY --from=build /app/dist/ms-inventario/browser /usr/share/nginx/html
COPY default.conf /etc/nginx/conf.d/default.conf



