FROM python:3

COPY /django_microservice/requirements.txt /api/requirements.txt

WORKDIR /api

RUN pip3 install -r requirements.txt

COPY /django_microservice /api

# ENTRYPOINT [ "python" ]

# CMD [ "manage.py", "runserver" ]
