# ------------------------
# Build stage (robusto)
# ------------------------
    FROM node:20-alpine AS build

    WORKDIR /app
    
    # 1) Copiamos solo manifests para cacheo
    COPY package*.json ./
    
    # 2) Endurecer npm: versión estable, tiempo y reintentos
    RUN npm i -g npm@11.5.2 && \
        npm config set registry https://registry.npmjs.org/ && \
        npm config set fetch-retries 5 && \
        npm config set fetch-retry-maxtimeout 300000 && \
        npm config set fetch-timeout 120000 && \
        npm config set prefer-online true && \
        npm cache clean --force
    
    # 3) Instalación con reintentos (evita artefactos corruptos)
    #    --legacy-peer-deps para evitar bloqueos de peer deps
    RUN set -eux; \
        for i in 1 2 3; do \
          echo ">>> npm install intento $i"; \
          npm install --no-audit --progress=false --legacy-peer-deps --force && break; \
          echo ">>> npm install falló, limpiando caché y reintentando..."; \
          npm cache clean --force; \
          sleep 2; \
        done
    
    # 4) Copiamos el resto del código
    COPY . .
    
    # 5) Validación explícita del paquete que te falla (path-key)
    #    Si este JSON está truncado, fallará aquí ANTES del build
    RUN node -e "const fs=require('fs'); JSON.parse(fs.readFileSync('node_modules/path-key/package.json','utf8'))"
    
    # 6) Build del frontend
    RUN npm run build
    
    # ------------------------
    # Production stage
    # ------------------------
    FROM nginx:alpine
    
    COPY --from=build /app/build /usr/share/nginx/html
    COPY nginx.conf /etc/nginx/conf.d/default.conf
    
    EXPOSE 80
    CMD ["nginx", "-g", "daemon off;"]