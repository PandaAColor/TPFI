"""proxy + singleton + observer"""
import argparse
import json
import logging
import socket
import threading
import uuid
from datetime import datetime
from decimal import Decimal

from .soporte.database_singleton import CorporateDataDB, CorporateLogDB
from .soporte.observer import Subject


def default_serializer(obj):
    """Convierte tipos que json no sabe serializar (como Decimal de DynamoDB)."""
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError(f"Tipo no serializable: {type(obj)}")


def handle_client(conn, db_data, db_log, subject):
    mantener_abierta = False
    try:
        data = conn.recv(65536)
        if not data:
            return
        request = json.loads(data.decode())
        action = request.get("ACTION")
        client_uuid = request.get("UUID")
        sesion = uuid.uuid4()
        ts = datetime.now().isoformat()

        if action == "get":
            id = request["ID"]
            db_log.log(client_uuid, sesion, "get", id, ts)
            item = db_data.get(id)
            conn.sendall(json.dumps(item or "Error", default=default_serializer).encode())

        elif action == "list":
            db_log.log(client_uuid, sesion, "list", "-", ts)
            items = db_data.list()
            conn.sendall(json.dumps(items, default=default_serializer).encode())

        elif action == "set":
            item = request.get("data", {})
            item.setdefault("id", request.get("ID"))
            db_log.log(client_uuid, sesion, "set", item.get("id"), ts)
            saved = db_data.set(item)
            conn.sendall(json.dumps(saved, default=default_serializer).encode())
            subject.notify(saved)

        elif action in ("subscribe", "suscribirse", "suscribe"):
            db_log.log(client_uuid, sesion, "subscribe", "-", ts)
            subject.subscribe(client_uuid, conn)
            mantener_abierta = True
            conn.sendall(json.dumps({"status": "subscribed"}, default=default_serializer).encode())

        else:
            conn.sendall(json.dumps("Error", default=default_serializer).encode())

    except Exception as e:
        logging.debug(f'Error: {e}')
        try:
            conn.sendall(json.dumps("Error", default=default_serializer).encode())
        except Exception:
            pass
    finally:
        if not mantener_abierta:
            conn.close()



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, default=8080, help="puerto")
    parser.add_argument("-v", action="store_true", help="modo para trace y debug")
    args = parser.parse_args()

    if args.v:
        logging.basicConfig(level=logging.DEBUG)

    db_data = CorporateDataDB()
    db_log = CorporateLogDB()
    subject = Subject()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("", args.p))
        server.listen(5)
        logging.debug(f'Servidor escuchando en: {args.p}')

        while True:
            conn, _ = server.accept()
            threading.Thread(
                target=handle_client,
                args=(conn, db_data, db_log, subject),
                daemon=True
            ).start()


if __name__ == "__main__":
    main()
