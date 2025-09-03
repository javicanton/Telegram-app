# Build stage
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm cache clean --force
RUN rm -rf node_modules package-lock.json
RUN npm install

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy the build output to replace the default nginx contents.
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 