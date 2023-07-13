from observer_rooms import Publisher, ConcreteObserver
from flask import request
from constructor import app, socketio
from flask_socketio import SocketIO, Namespace, emit, send, join_room, leave_room, close_room, rooms, disconnect

websocket_clients = Publisher(socketio=socketio)

class _TestNamespace(Namespace):
    def on_connect(self):
        new_observer = ConcreteObserver(request.sid, self.namespace)
        websocket_clients.attach(new_observer)
        send("Connected")
        print(f'Client connected to {self.namespace}')


    def on_disconnect(self):
        with app.app_context():
            websocket_clients.detach(request.sid)
            print(f'Client {request.sid} disconnected')
            send('diconnected')

    def on_event(self):
        websocket_clients.notify()

    def on_error_default(self, e):
        print(f'chat_error_handler. An error has occurred: {e}')
        app.logger.error(e)
        send("Error received")


class Dashboard(_TestNamespace):
    def on_hala(self):
        send("HALA")