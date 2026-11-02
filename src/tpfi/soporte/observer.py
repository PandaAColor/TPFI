"""Gestiona los sockets suscriptos"""

import json


class Subject:
    """Sujeto observado - sockets suscriptos"""

    def __init__(self):
        self._observers = {}

    def subscribe(self, uuid, socket):
        self._observers[uuid] = socket

    def notify(self, data):
        payload = json.dumps(data).encode()
        for socket in self._observers.values():
            try:
                socket.sendall(payload)
            except Exception:
                continue
