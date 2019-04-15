FROM node:alpine

WORKDIR /app

RUN apk update && apk add git

RUN npm update && npm i -g redoc-cli

COPY ./docs.yaml /swagger/docs.yaml

RUN redoc-cli bundle /swagger/docs.yaml -o /swagger/static/index.html

FROM nginx:alpine

COPY ./auth /etc/nginx/auth

COPY ./host.conf /etc/nginx/conf.d/default.conf

COPY --from=0 /swagger/static/index.html /usr/share/nginx/html
