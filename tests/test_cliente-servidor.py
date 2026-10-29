"""Pruebas del protocolo cliente-servidor."""
import json
from unittest import mock

from src.tpfi.singletonproxyobserver import handle_client


class FakeConn:
    """Simula la conexión del cliente para capturar lo que envía el servidor."""
    def __init__(self, request=b""):
        self.request = request
        self.sent = b""

    def recv(self, bufsize):
        return self.request

    def sendall(self, data):
        self.sent += data

    def close(self):
        pass

def test_handle_client_responde_a_list():
    conn = FakeConn(json.dumps({"UUID": "123", "ACTION": "list"}).encode())
    handle_client(conn, db_data=mock.Mock(), db_log=mock.Mock(), subject=mock.Mock())
    assert conn.sent != b""


def test_handle_client_responde_error_si_pedido_invalido():
    conn = FakeConn()
    with mock.patch.object(conn, "recv", return_value=b"no es json"):
        handle_client(conn, db_data=mock.Mock(), db_log=mock.Mock(), subject=mock.Mock())

    # Ante un pedido inválido, responde "Error"
    assert json.loads(conn.sent) == "Error"


def test_handle_client_get_serializa_decimal():
    conn = FakeConn()
    # db_data.get devuelve un item con Decimal (como DynamoDB real)
    db_data = mock.Mock()
    db_data.get.return_value = {"id": "x", "idreq": 224}  # int normal

    with mock.patch.object(conn, "recv", return_value=json.dumps(
        {"UUID": "123", "ID": "x", "ACTION": "get"}
    ).encode()):
        handle_client(conn, db_data=db_data, db_log=mock.Mock(), subject=mock.Mock())

    # La respuesta debe ser JSON válido (no romperse con Decimal)
    respuesta = json.loads(conn.sent)
    assert respuesta["id"] == "x"
