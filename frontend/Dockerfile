# ------------------------
# Build stage (Node 18 LTS)
# ------------------------
    FROM node:18-alpine AS build

    WORKDIR /app
    # Herramientas mínimas por si alguna dependencia compila nativos
    RUN apk add --no-cache python3 make g++ tar
    
    # 1) Copiamos SOLO los manifests (mejor caché)
    COPY package*.json ./
    
    # 2) NPM estable + limpieza
    RUN npm i -g npm@10 && npm cache clean --force
    
    # 3) Instala EXACTO según el lockfile (que ya tienes sincronizado en el repo)
    #    Usa --legacy-peer-deps por compat. con react-scripts antiguos
    RUN npm ci --no-audit --progress=false --legacy-peer-deps
    
    # 4) Copiamos el resto del código y construimos
    COPY . .
    # (debug opcional) comprobar versión de Node usada en build
    RUN node -v
    RUN npm run build
    
    # ------------------------
    # Production stage
    # ------------------------
    FROM nginx:alpine
    
    # Servimos el estático generado por React
    COPY --from=build /app/build /usr/share/nginx/html
    
    # Config de nginx del proyecto
    COPY nginx.conf /etc/nginx/conf.d/default.conf
    
    EXPOSE 80
    CMD ["nginx", "-g", "daemon off;"]