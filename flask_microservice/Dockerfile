FROM python:3.8-slim-buster

COPY /flask_microservice /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "wsgi.py" ]
