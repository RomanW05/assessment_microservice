from abc import ABC, abstractmethod


class ISubject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def attach(self, observer) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass

    

class IObserver(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: ISubject) -> None:
        """
        Receive update from subject.
        """
        pass


class IMyNamespace(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def on_connect(self):
        pass

    @abstractmethod
    def on_disconnect(self):
        pass

    @abstractmethod
    def on_event(self):
        pass
