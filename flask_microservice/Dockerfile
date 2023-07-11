FROM python:3.8-slim-buster

COPY /flask_microservice/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY /flask_microservice /app

ENTRYPOINT [ "python" ]

CMD [ "wsgi.py" ]
