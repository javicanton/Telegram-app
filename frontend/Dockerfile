# frontend/Dockerfile
FROM node:18.18.0-alpine AS build
WORKDIR /app

# Manifiestos primero (cache de deps)
COPY package.json package-lock.json ./

# Instalar dependencias de forma simple
RUN npm install

# Código (sin node_modules)
COPY . .

# Actualizar browserslist y build estático
RUN npx update-browserslist-db@latest && npm run build

# --- Runtime Nginx ---
FROM nginx:alpine
WORKDIR /usr/share/nginx/html
# Serviremos en 80 y 8080 para no depender de qué puerto apunte el TG
EXPOSE 80 8080
# Estático generado
COPY --from=build /app/build /usr/share/nginx/html
# Conf con healthcheck, SPA fallback y proxy opcional a /api
COPY nginx.conf /etc/nginx/conf.d/default.conf
