# ------------------------
# Build stage
# ------------------------
    FROM node:20-alpine AS build

    WORKDIR /app
    
    # Copiamos solo los manifests primero para aprovechar la caché de Docker
    COPY package*.json ./
    
    # Instalamos dependencias con lockfile (más rápido y reproducible)
    # Flags: sin auditoría, sin progreso, sin conflictos de peer deps
    RUN npm install --no-audit --progress=false --legacy-peer-deps
        
    # Copiamos el resto del código y construimos
    COPY . .
    RUN npm run build
    
    # ------------------------
    # Production stage
    # ------------------------
    FROM nginx:alpine
    
    # Copiamos la build de React al nginx
    COPY --from=build /app/build /usr/share/nginx/html
    
    # Config custom de nginx
    COPY nginx.conf /etc/nginx/conf.d/default.conf
    
    EXPOSE 80
    
    CMD ["nginx", "-g", "daemon off;"]