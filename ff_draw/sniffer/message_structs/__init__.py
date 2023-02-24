import enum

from ..enums import ZoneClient, ZoneServer, ChatServer, ChatClient, ActorControlId


class TypeMap:
    def __init__(self):
        self.data = {}
        self.get = self.data.get

    def set(self, pno: enum.Enum):
        def wrapper(cls):
            self.data[pno] = cls
            return cls

        return wrapper
