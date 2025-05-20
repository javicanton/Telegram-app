# Etapa de construcción
FROM node:18-alpine as builder

# Configurar variables de entorno
ENV NODE_ENV=production

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias con optimizaciones
RUN npm install --production --no-optional && \
    npm cache clean --force && \
    rm -rf /root/.npm

# Copiar el resto del código
COPY . .

# Construir la aplicación
RUN npm run build && \
    rm -rf node_modules

# Etapa de producción
FROM nginx:stable-alpine

# Copiar configuración de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar archivos de construcción
COPY --from=builder /app/build /usr/share/nginx/html

# Limpiar caché de nginx
RUN rm -rf /var/cache/nginx/*

# Exponer puerto
EXPOSE 80

# Iniciar nginx
CMD ["nginx", "-g", "daemon off;"] 