# ------------------------
# Build stage
# ------------------------
    FROM node:20-alpine AS build

    WORKDIR /app
    
    # Copiamos solo manifests para aprovechar caché
    COPY package*.json ./
    
    # Endurecer npm y forzar descarga limpia (evitar artefactos corruptos)
    RUN npm config set fetch-retries 5 \
     && npm config set fetch-retry-maxtimeout 300000 \
     && npm config set fetch-timeout 120000 \
     && npm cache clean --force \
     && npm install --no-audit --progress=false --legacy-peer-deps --prefer-online
    
    # Copiamos el resto y construimos
    COPY . .
    RUN npm run build
    
    # ------------------------
    # Production stage
    # ------------------------
    FROM nginx:alpine
    
    COPY --from=build /app/build /usr/share/nginx/html
    COPY nginx.conf /etc/nginx/conf.d/default.conf
    
    EXPOSE 80
    CMD ["nginx", "-g", "daemon off;"]