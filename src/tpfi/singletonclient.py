"""Cliente singleton - get/set/list"""
import argparse
import json
import logging
import socket
import sys
import uuid


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required = True, help = "archivo de entrada JSON")
    parser.add_argument("-o", help="archivo de salida JSON(opcional)")
    parser.add_argument("-p", type=int, default=8080, help="puerto del servidor")
    parser.add_argument("-v", action= "store_true", help="modo para trace y debug")
    parser.add_argument("-d", help="JSON de entrada directo (alternativa a -i)")

    args = parser.parse_args()

    if args.v:
        logging.basicConfig(level=logging.DEBUG)

    with open(args.i) as f:
        request = json.load(f)

    #Si no viene un UUID agrega el de la CPU
    request.setdefault("UUID", str(uuid.getnode()))
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", args.p))
            s.sendall(json.dumps(request).encode())
            data = s.recv(65536)
    except ConnectionRefusedError:
        print("Servidor no disponible")
        sys.exit(1)

    response = data.decode()
    if args.o:
        with open(args.o, "w") as f:
            f.write(response)

        if args.d:
            request = json.loads(args.d)
    else:
        with open(args.i) as f:
            request = json.load(f)


    
    print(response)


if __name__ == "__main__":
    main()
