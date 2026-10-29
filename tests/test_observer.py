"""Pruebas del patrón Observer."""
from src.tpfi.soporte.observer import Subject


class FakeSocket:
    def __init__(self):
        self.sent = []

    def sendall(self, data):
        self.sent.append(data)


def test_suscribe_and_notify():
    subject = Subject()
    sock = FakeSocket()
    subject.subscribe("uuid-1", sock)
    subject.notify({"id": "x"})
    assert len(sock.sent) == 1
