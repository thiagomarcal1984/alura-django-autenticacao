FROM python:3.8

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
ENV DJANGO_SUPERUSER_USERNAME=thiago
ENV DJANGO_SUPERUSER_PASSWORD=thiago
ENV DJANGO_SUPERUSER_EMAIL=thiago@thiago.com

# RUN python manage.py migrate
CMD python manage.py runserver
