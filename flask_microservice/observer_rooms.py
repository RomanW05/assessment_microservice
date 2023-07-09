from interfaces import ISubject, IObserver
# from flask_socketio import SocketIO, emit
# import random


class dashboard(ISubject):
    def __init__(self, socketio) -> None:
        self.socket = socketio
        self.observers = []

    def attach(self, observer: IObserver) -> None:
        print("Subject: Attached an observer.")
        self.observers.append(observer)

    def detach(self, observer: IObserver) -> None:
        self.observers.remove(observer)

    def notify(self) -> None:
        print("Subject: Notifying observers...")
        for observer in self.observers:
            self.socket.emit('my_response',{'data': message['data'], 'count': session['receive_count']}, to=message['room'], broadcast=True)
            observer.update(self)
    
    def _some_business_logic(self, price) -> None:
        print("\nSubject: I'm doing something important.")
        self._state = price

        print(f"Subject: My state has just changed to: {self._state}")
        self.notify()
    
    


class ConcreteObserver(IObserver):
    def __init__(self, sid) -> None:
        self.sid = sid

    def update(self, subject: IObserver) -> None:
        if subject._state < 3:
            print("ConcreteObserver: Reacted to the event")