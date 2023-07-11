FROM python:3.8-slim-buster

COPY /flask_microservice /app

WORKDIR /app

# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0

RUN pip3 install -r requirements.txt
# RUN pip install hypercorn
# # RUN pip install asgiref
# # RUN pip install daphne
# RUN pip install uvicorn
# RUN pip install simple-websocket
# RUN pip install flask-socketio==5.2.0
# RUN pip install waitress
# RUN pip install gevent
# RUN pip install gevent-websocket

# COPY ./flask_microservice .

# EXPOSE 8000
# CMD [ "daphne", "-b", "0.0.0.0", "-p", "8000", "app:wsgi" ]
# CMD ["hypercorn", "app:wsgi"]
ENTRYPOINT [ "python" ]

CMD [ "wsgi.py" ]
# CMD ["waitress-serve", "--call", "app:create_app"]