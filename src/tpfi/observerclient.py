"""se suscribe y escucha notificaciones"""
import argparse
import json
import logging
import socket
import time
import uuid


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", default="localhost", help="hostname")
    parser.add_argument("-p", type=int, default=8080, help = "puerto")
    parser.add_argument("-o", help="archivo de salida JSON (opcional)")
    parser.add_argument("-v", action= "store_true", help="modo para trace y debug")
    parser.add_argument("-r", "--retry", type=int, default=30, help="Segundos entre reintentos de conexión")
    parser.add_argument("-d", help="JSON de entrada directo (alternativa a -i)")

    args = parser.parse_args()

    if args.v:
        logging.basicConfig(level=logging.DEBUG)

    request = {"UUID": str(uuid.getnode()), "ACTION": "subscribe"}

    if args.d:
        request = json.loads(args.d)
    else:
        with open(args.i) as f:
            request = json.load(f)

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((args.s, args.p))
                s.sendall(json.dumps(request).encode())
                while True:
                    data = s.recv(65536)
                    if not data:
                        break
                    text = data.decode()
                    if args.o:
                        with open(args.o, "a") as f:
                            f.write(text + "\n")
                    else:
                        print(text)
        except (ConnectionAbortedError, OSError):
            logging.debug("Servidor caido, reintentando en %ss...", args.retry)
            time.sleep(args.retry)

if __name__ == "__main__":
    main()
