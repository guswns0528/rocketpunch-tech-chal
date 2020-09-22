FROM node:lts-alpine as builder

RUN yarn global add http-server

WORKDIR /app

COPY package*.json ./
RUN yarn install
COPY . .
RUN yarn build

FROM nginx:stable-alpine as prod
COPY --from=builder /app/builder /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
