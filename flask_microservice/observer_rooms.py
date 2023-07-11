from interfaces import ISubject, IObserver


class Publisher(ISubject):
    def __init__(self, socketio) -> None:
        self.socket = socketio
        self._observers = {}

    def attach(self, observer: IObserver) -> None:
        print("Subject: Attached an observer.")
        self._observers[observer.sid] = observer

    def detach(self, sid: str) -> None:
        self._observers.pop(sid)

    def notify(self) -> None:
        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)
    
    def emit_price(self, price: float) -> None:
        print("Price updated")
        self.price = price

        print(f"Subject: Price just changed to: {self.price}")
        self.notify()    
    

class ConcreteObserver(IObserver):
    def __init__(self, sid: str, room: str):
        self.sid = sid

    def update(self, subject: IObserver) -> None:
        # self.socket.emit('my_response',{'price': self.price}, namespace=self.room, broadcast=True)
        print("ConcreteObserver: Reacted to the event")


