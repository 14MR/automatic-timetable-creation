FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN pip install uwsgi

EXPOSE 80

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

USER $MOD_WSGI_USER:$MOD_WSGI_GROUP

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:80