# Etapa 1: construir la app React
FROM node:18-alpine AS builder

# Establecer variables de entorno
ENV NODE_ENV=production

WORKDIR /app

# Copiar archivos de dependencias primero
COPY package*.json ./

# Instalar dependencias
RUN npm ci

# Copiar el resto del código
COPY . .

# Construir la aplicación
RUN npm run build

# Etapa 2: servir con Nginx
FROM nginx:stable-alpine

# Copiar configuración personalizada de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar los archivos construidos
COPY --from=builder /app/build /usr/share/nginx/html

# Crear usuario no root
RUN adduser -D -H -u 101 -s /sbin/nologin nginx || true

# Exponer puerto
EXPOSE 80

# Comando para ejecutar nginx
CMD ["nginx", "-g", "daemon off;"] 