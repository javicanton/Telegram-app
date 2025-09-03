# ------------------------
# Build stage (Node 18 LTS)
# ------------------------
    FROM node:18-alpine AS build

    WORKDIR /app
    RUN apk add --no-cache python3 make g++ tar
    
    # Manifests primero (aprovecha caché)
    COPY package*.json ./
    
    # NPM estable + timeouts razonables
    RUN npm i -g npm@10 && \
        npm config set registry https://registry.npmjs.org/ && \
        npm config set fetch-retries 5 && \
        npm config set fetch-retry-maxtimeout 300000 && \
        npm config set fetch-timeout 120000 && \
        npm cache clean --force
    
    # Instala EXACTO según el lockfile (ya actualizado con overrides)
    RUN npm ci --no-audit --progress=false --legacy-peer-deps
    
    # Copia el resto y build
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