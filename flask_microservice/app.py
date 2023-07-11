from flask import Flask, render_template, session, copy_current_request_context, request
from flask_socketio import SocketIO, Namespace, emit, send, join_room, leave_room, close_room, rooms, disconnect
import random
from config import config
import json
from engineio.payload import Payload
from observer_rooms import Publisher, ConcreteObserver
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import logging
from asgiref.wsgi import WsgiToAsgi


# Setup logs
# logger= logging.getLogger()
# logger.setLevel(logging.DEBUG) # or whatever
# handler = logging.FileHandler('logs/debug.log', 'a', 'utf-8') # or whatever
# handler.setFormatter(logging.Formatter('%(name)s %(message)s')) # or whatever
# logger.addHandler(handler)

# Configure app
secret = config()
app = Flask(__name__, template_folder='static/templates', static_folder='static')
app.config['SECRET_KEY'] = secret
app.use_reloader=False
async_mode = None
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*')
Payload.max_decode_packets = 16

# Setup logs
if app.debug is not True:   
    import logging
    from logging.handlers import TimedRotatingFileHandler
    logname = "logs/websocket.log"
    file_handler = TimedRotatingFileHandler(logname, when="midnight", backupCount=30, utc=True)
    file_handler.suffix = "%Y%m%d"
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

# Load interfaces
websocket_clients = Publisher(socketio=socketio)

# Define Class-based Namespaces
class MyNamespace(Namespace):
    def on_connect(self):
        new_observer = ConcreteObserver(request.sid, self.namespace)
        websocket_clients.attach(new_observer)
        print(f'Client connected to {self.namespace}')

    def on_disconnect(self):
        with app.app_context():
            websocket_clients.detach(request.sid)
            print(f'Client {request.sid} disconnected')

    def on_event(self):
        websocket_clients.notify()


# Namespaces instantiation
socketio.on_namespace(MyNamespace('/dashboard'))


@socketio.on_error_default
def error_handler(e):
    print(f'chat_error_handler. An error has occurred: {e}')
    app.logger.error(e)


def price_change():
    price = float(round(random.uniform(0.01, 99.99), 2))
    # if len(websocket_clients.observers) > 0:
    with app.app_context():
        room = "/dashboard"
        emit('message', {'count': price, 'data': 'message sent'}, broadcast=True, namespace=room)


def price_alert(price, room):
    with app.app_context():
        emit('message', {'price': price}, broadcast=True, namespace=room)


def backround_task_manager():
    print('background task manager started')
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=price_change, trigger="interval", seconds=1)
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

def create_app():
   backround_task_manager()
   return WsgiToAsgi(socketio.run(
       app, host='0.0.0.0', port=8000
       ))



