FROM node:18-alpine AS build
WORKDIR /app
RUN apk add --no-cache python3 make g++ tar
COPY package*.json ./
RUN npm i -g npm@10 && npm cache clean --force
RUN npm ci --no-audit --progress=false --legacy-peer-deps
COPY . .
RUN node -v
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]