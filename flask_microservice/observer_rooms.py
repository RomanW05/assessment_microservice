from interfaces import ISubject, IObserver


class Publisher(ISubject):
    def __init__(self, socketio) -> None:
        self.socket = socketio
        self._observers = {}

    def attach(self, observer: IObserver) -> None:
        self._observers[observer.sid] = observer
        print(f'Subject: Attached observer {observer}')

    def detach(self, sid: str) -> None:
        del self._observers[sid]
        print(f'Observer {sid} detached')

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
        self.room = room

    def update(self) -> None:
        # self.socket.emit('my_response',{'price': self.price}, namespace=self.room, broadcast=True)
        print("ConcreteObserver: Reacted to the event")

