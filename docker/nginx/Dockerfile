FROM registry.gitlab.com/automatic-timetable-creation/backend:latest

RUN python manage.py collectstatic --no-input

FROM nginx:1.15.8-alpine

COPY ./host.conf /etc/nginx/conf.d/default.conf

COPY --from=0 /app/static /usr/share/nginx/html/static
