FROM python:3.8-slim-buster

COPY /django_microservice /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "wsgi.py" ]
