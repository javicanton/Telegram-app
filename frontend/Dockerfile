# ------------------------
# Build stage (Node 18 LTS, instalación robusta)
# ------------------------
    FROM node:18-alpine AS build

    WORKDIR /app
    RUN apk add --no-cache python3 make g++ tar
    
    # Copiamos manifests primero (caché)
    COPY package*.json ./
    
    # npm estable + red robusta (sin 'jobs')
    RUN npm i -g npm@10 && \
        npm config set registry https://registry.npmjs.org/ && \
        npm config set fetch-retries 5 && \
        npm config set fetch-retry-maxtimeout 300000 && \
        npm config set fetch-timeout 120000 && \
        npm cache clean --force
    
    # Instala EXACTO según lockfile con reintentos
    RUN set -eux; \
      for i in 1 2 3; do \
        echo ">>> npm ci intento $i"; \
        npm ci --no-audit --progress=false --legacy-peer-deps && break; \
        echo ">>> npm ci falló, limpiando caché y reintentando..."; \
        npm cache clean --force; rm -rf node_modules; sleep 2; \
      done
    
    # Valida path-key; si está truncado, rehidrátalo con npm pack
    RUN node -e "try{JSON.parse(require('fs').readFileSync('node_modules/path-key/package.json','utf8'));process.exit(0)}catch(e){process.exit(1)}" \
     || ( \
          echo '>>> Reparando node_modules/path-key con npm pack…' && \
          rm -rf node_modules/path-key && \
          npm pack path-key@4.0.0 --silent && \
          tar -xzf path-key-*.tgz -C node_modules && \
          mv node_modules/package node_modules/path-key && \
          rm -f path-key-*.tgz && \
          node -e "JSON.parse(require('fs').readFileSync('node_modules/path-key/package.json','utf8'))" \
        )
    
    # Copia resto del código y compila
    COPY . .
    RUN node -v
    RUN npm run build
    
    # ------------------------
    # Production stage
    # ------------------------
    FROM nginx:alpine
    COPY --from=build /app/build /usr/share/nginx/html
    COPY nginx.conf /etc/nginx/conf.d/default.conf
    EXPOSE 80
    CMD ["nginx", "-g", "daemon off;"]