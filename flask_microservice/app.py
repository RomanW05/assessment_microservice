from threading import Lock
from flask import Flask, render_template, session, copy_current_request_context, request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
import random
from config import config
import json
from engineio.payload import Payload
import time
from observer_rooms import dashboard, ConcreteObserver
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import logging
logging.basicConfig(filename='logs/debug.log', encoding='utf-8', level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
logging.error('And non-ASCII stuff, too, like Øresund and Malmö')


Payload.max_decode_packets = 16

secret = config()
app = Flask(__name__, template_folder='static/templates', static_folder='static')
app.config['SECRET_KEY'] = secret

async_mode = None
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*')

dashboard_prices = dashboard(socketio=socketio)

@app.route('/')
def index():
    return render_template('index2.html', async_mode=socketio.async_mode), 200


@socketio.event
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


@socketio.on('connect')
def handleConnect():
    new_observer = ConcreteObserver(request.sid)
    dashboard_prices.attach(new_observer)



@socketio.on('disconnect')
def disconnect_():
    with app.app_context():
        dashboard_prices.detach(request.sid)
        print('Client disconnected', request.sid)


@socketio.on_error()
def chat_error_handler(e):
    print('chat_error_handler\n\n\nchat_error_handler: An error has occurred: ' + str(e))


def price_change():
    price = float(round(random.uniform(0.01, 99.99), 2))
    if len(dashboard_prices.observers) > 0:
        with app.app_context():
            emit('message', {'count': price, 'data': 'message sent'}, broadcast=True, namespace='')


def backround_task_manager():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=price_change, trigger="interval", seconds=1)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    backround_task_manager()
    socketio.run(app, port=8000)
