FROM node:8.15.1-alpine

WORKDIR /app

RUN apk update && apk add git

RUN npm update && npm i -g redoc-cli

COPY ./swagger/docs.yaml /swagger/docs.yaml

RUN redoc-cli bundle /swagger/docs.yaml -o /swagger/static/index.html

FROM nginx:1.15.8-alpine

COPY ./docker/nginx-docs/auth /etc/nginx/auth

COPY ./docker/nginx-docs/host.conf /etc/nginx/conf.d/default.conf

COPY --from=0 /swagger/static/index.html /usr/share/nginx/html
