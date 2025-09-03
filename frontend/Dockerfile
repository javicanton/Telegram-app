# ------------------------
# Build stage (robusto)
# ------------------------
    FROM node:20-alpine AS build

    WORKDIR /app
    
    # Opcional: herramientas (tar ya viene con busybox, pero añadimos curl si lo necesitas en otros pasos)
    RUN apk add --no-cache tar
    
    # Copiamos manifests y endurecemos npm
    COPY package*.json ./
    RUN npm i -g npm@11.5.2 && \
        npm config set registry https://registry.npmjs.org/ && \
        npm config set fetch-retries 5 && \
        npm config set fetch-retry-maxtimeout 300000 && \
        npm config set fetch-timeout 120000 && \
        npm config set prefer-online true && \
        npm cache clean --force
    
    # Instalación con reintentos (evita artefactos corruptos)
    RUN set -eux; \
      for i in 1 2 3; do \
        echo ">>> npm install intento $i"; \
        npm install --no-audit --progress=false --legacy-peer-deps --force && break; \
        echo ">>> npm install falló, limpiando caché y reintentando..."; \
        npm cache clean --force; \
        sleep 2; \
      done
    
    # Copiamos código
    COPY . .
    
    # --- Reparación path-key si viene corrupto (sin curl) ---
    RUN node -e "try{JSON.parse(require('fs').readFileSync('node_modules/path-key/package.json','utf8'));process.exit(0)}catch(e){process.exit(1)}" \
     || ( \
          echo '>>> Reparando node_modules/path-key con npm pack…' && \
          rm -rf node_modules/path-key && \
          npm pack path-key@latest --silent && \
          tar -xzf path-key-*.tgz -C node_modules && \
          mv node_modules/package node_modules/path-key && \
          rm -f path-key-*.tgz \
        )
    
    # Validación final antes de build
    RUN node -e "const fs=require('fs'); JSON.parse(fs.readFileSync('node_modules/path-key/package.json','utf8'))"
    
    # Build
    RUN npm run build
    
    # ------------------------
    # Production stage
    # ------------------------
    FROM nginx:alpine
    
    COPY --from=build /app/build /usr/share/nginx/html
    COPY nginx.conf /etc/nginx/conf.d/default.conf
    
    EXPOSE 80
    CMD ["nginx", "-g", "daemon off;"]