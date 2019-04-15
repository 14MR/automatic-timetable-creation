FROM swaggerapi/swagger-codegen-cli:latest

COPY ./docs.yaml /swagger/docs.yml

ENTRYPOINT "/bin/sh"
#ENTRYPOINT ["java", "-jar", "/opt/swagger-codegen-cli/swagger-codegen-cli.jar"]
#
#RUN swagger-codegen generate -i /swagger/docs.yml -l html2 -o /swagger/static/

#FROM nginx:1.15.8-alpine
#
#COPY ./host.conf /etc/nginx/conf.d/default.conf
#
#COPY ./auth /etc/nginx/auth
#
#COPY --from=0 /app/static /usr/share/nginx/html/static
#
