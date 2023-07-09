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

Payload.max_decode_packets = 50

thread = None
thread_lock = Lock()

secret = config()
app = Flask(__name__, template_folder='static/templates', static_folder='static')
app.config['SECRET_KEY'] = secret

async_mode = None
socketio = SocketIO(app, async_mode=async_mode)

dashboard_prices = dashboard(socketio=socketio)

# def background_thread():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         socketio.sleep(10)
#         count += 1
#         socketio.emit('my_response',
#                       {'data': 'Server generated event', 'count': count})


@app.route('/')
def index():
    
    return render_template('index2.html', async_mode=socketio.async_mode)




@socketio.event
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.event
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})







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







# @socketio.event
# def connect():
#     global thread
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(background_thread)
#     emit('my_response', {'data': 'Connected', 'count': 0}, broadcast=True)

@socketio.on('connect')
def handleConnect():
    print('New user connected')
    # observer_a = ConcreteObserver()
    new_observer = ConcreteObserver(request.sid)
    dashboard_prices.attach(new_observer)

    # print('Someone connected')
    emit('message', 'A user has joined', broadcast=True)



@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)




@socketio.on_error()
def chat_error_handler(e):
    print('An error has occurred: ' + str(e))



@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit(username + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit(username + ' has left the room.', to=room)



@socketio.on('join_dashroom')
def on_join(data):
    sid = request.sid
    room = 'dashboard'
    join_room(room)
    print(f'{sid} joined room {room}')
    emit('message', {'count': 'asd', 'data': f'{sid} has entered the room.'}, to='/room')





def price_change():
    price = float(round(random.uniform(0.01, 99.99), 2))
    # import sys
    # print(dashboard_prices.observers)
    # sys.exit()
    if len(dashboard_prices.observers) != 0:
        with app.app_context():
            # print('broadcasting')
            emit('message', {'count': price, 'data': 'message sent'}, broadcast=True, namespace='/dashboard')
            















if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=price_change, trigger="interval", seconds=1)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    socketio.run(app, port=8000)
