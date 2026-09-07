"""Transporte TCP local para probar los algoritmos sin depender del servidor XMPP."""

import json
import socket
import threading


class Transport:
    def __init__(self, host, port, on_packet):
        self.on_packet = on_packet
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((host, port))
        self._server.listen()
        threading.Thread(target=self._accept_loop, daemon=True).start()

    def _accept_loop(self):
        while True:
            conn, _ = self._server.accept()
            threading.Thread(target=self._handle_connection, args=(conn,), daemon=True).start()

    def _handle_connection(self, conn):
        with conn:
            buffer = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                buffer += chunk
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    if line:
                        self.on_packet(json.loads(line.decode("utf-8")))

    def send(self, host, port, packet):
        try:
            with socket.create_connection((host, port), timeout=2) as conn:
                conn.sendall((json.dumps(packet) + "\n").encode("utf-8"))
        except OSError:
            pass  # ponytail: nodo caido o inalcanzable, se descarta sin reintentos
