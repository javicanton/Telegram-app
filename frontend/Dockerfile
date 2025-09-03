# ------------------------
# Build stage (robusto)
# ------------------------
    FROM node:20-alpine AS build

    WORKDIR /app
    
    # Herramientas mínimas para descargar/verificar
    RUN apk add --no-cache curl tar
    
    # Copiamos solo manifests para cachear
    COPY package*.json ./
    
    # Endurecemos npm + limpiamos caché
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
    
    # Copiamos el resto del código
    COPY . .
    
    # --- REPARACIÓN ESPECÍFICA path-key si viene corrupto ---
    # Si el JSON de path-key está truncado, lo rehidratamos desde el tarball oficial
    RUN node -e "try{JSON.parse(require('fs').readFileSync('node_modules/path-key/package.json','utf8'));process.exit(0)}catch(e){process.exit(1)}" \
     || ( \
          echo '>>> Reparando node_modules/path-key desde el registro…' && \
          PK_TARBALL=$(node -e "p=require('child_process').execSync('npm view path-key dist.tarball').toString().trim();process.stdout.write(p)") && \
          echo \"Tarball: ${PK_TARBALL}\" && \
          curl -fsSL \"$PK_TARBALL\" -o /tmp/path-key.tgz && \
          tar -tzf /tmp/path-key.tgz >/dev/null && \
          rm -rf node_modules/path-key && \
          mkdir -p /tmp/path-key && \
          tar -xzf /tmp/path-key.tgz -C /tmp/path-key && \
          mv /tmp/path-key/package node_modules/path-key \
       )
    
    # Validación final antes de build
    RUN node -e "const fs=require('fs'); JSON.parse(fs.readFileSync('node_modules/path-key/package.json','utf8'))"
    
    # Build del frontend
    RUN npm run build
    
    # ------------------------
    # Production stage
    # ------------------------
    FROM nginx:alpine
    
    COPY --from=build /app/build /usr/share/nginx/html
    COPY nginx.conf /etc/nginx/conf.d/default.conf
    
    EXPOSE 80
    CMD ["nginx", "-g", "daemon off;"]