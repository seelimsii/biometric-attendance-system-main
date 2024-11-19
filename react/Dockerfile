# Stage 1: Build React app
FROM node:16 AS build

WORKDIR /react

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Use Nginx to serve the React app
FROM nginx:1.25

COPY --from=build react/dist/ /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 6000
EXPOSE 6000

CMD ["nginx", "-g", "daemon off;"]