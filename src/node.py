"""Un nodo de la red: hilo de forwarding (llega por el socket) + hilo de routing
(hellos e info periodicos) corriendo al mismo tiempo, como pide el enunciado.
"""

import queue
import threading
import time

from . import packet as pkt
from .routing.flooding import broadcast_targets
from .transport import Transport

ROUTING_INTERVAL = 5  # segundos entre rondas de hello/info
# ponytail: no hay deteccion de vecinos caidos (timeout de hello), solo se
# reacciona a lo que llega. Agregar si se necesita tolerancia real a fallos.


class Node:
    def __init__(self, node_id, host, port, neighbors, addresses, algorithm, algorithm_name):
        self.id = node_id
        self.neighbors = neighbors
        self.addresses = addresses
        self.algorithm = algorithm
        self.algorithm_name = algorithm_name

        self.lock = threading.Lock()
        self.inbox = queue.Queue()
        self.seen_messages = set()

        self.transport = Transport(host, port, self._on_receive)

    def start(self):
        threading.Thread(target=self._routing_loop, daemon=True).start()

    # --- forwarding: se ejecuta en el hilo de la conexion entrante ---

    def _on_receive(self, packet):
        ptype = packet.get("type")
        if ptype == "hello":
            self.algorithm.on_hello(packet, pkt.get_header(packet, "hop"))
        elif ptype == "info":
            self.inbox.put(packet)
        elif ptype == "message":
            self._handle_message(packet)

    def _handle_message(self, packet):
        msg_id = pkt.get_header(packet, "id")
        if msg_id is not None:
            with self.lock:
                if msg_id in self.seen_messages:
                    return
                self.seen_messages.add(msg_id)

        if packet["to"] == self.id:
            print(f"[{self.id}] mensaje de {packet['from']}: {packet['payload']}")
            return

        packet["ttl"] -= 1
        if packet["ttl"] <= 0:
            return

        from_neighbor = pkt.get_header(packet, "hop")
        targets = self.algorithm.get_forward_targets(packet["to"], from_neighbor)
        for target in targets:
            self._send_to_neighbor(target, packet)

    # --- routing: hilo aparte, procesa info y manda hello/info periodicos ---

    def _routing_loop(self):
        last_broadcast = 0
        while True:
            try:
                packet = self.inbox.get(timeout=1)
                self._process_info(packet)
            except queue.Empty:
                pass

            if time.time() - last_broadcast >= ROUTING_INTERVAL:
                self._broadcast_periodic()
                last_broadcast = time.time()

    def _process_info(self, packet):
        from_neighbor = pkt.get_header(packet, "hop")
        with self.lock:
            is_new = self.algorithm.on_info(packet, from_neighbor)

        if is_new and self.algorithm.floods_info:
            for target in broadcast_targets(self.neighbors, from_neighbor):
                self._send_to_neighbor(target, packet)

    def _broadcast_periodic(self):
        for neighbor in self.neighbors:
            hello = pkt.build_packet(self.algorithm_name, "hello", self.id, neighbor, 1, {})
            self._send_to_neighbor(neighbor, hello)

        with self.lock:
            payloads = self.algorithm.build_info_payloads()

        for payload in payloads:
            for neighbor in self.neighbors:
                info = pkt.build_packet(self.algorithm_name, "info", self.id, neighbor, 8, payload)
                self._send_to_neighbor(neighbor, info)

    # --- utilidades ---

    def _send_to_neighbor(self, neighbor_id, packet):
        address = self.addresses.get(neighbor_id)
        if address is None:
            return
        host, port = address
        self.transport.send(host, port, pkt.with_header(packet, "hop", self.id))

    def send_message(self, dest, text):
        if dest == self.id:
            print("no te podes mandar un mensaje a vos mismo")
            return

        message = pkt.build_packet(
            self.algorithm_name, "message", self.id, dest, ttl=15,
            payload=text, headers=[{"id": pkt.new_message_id()}],
        )
        with self.lock:
            targets = self.algorithm.get_forward_targets(dest, None)
        for target in targets:
            self._send_to_neighbor(target, message)

    def print_table(self):
        next_hops = getattr(self.algorithm, "next_hops", None)
        if next_hops is None:
            print("flooding no arma tabla de ruteo")
            return
        if not next_hops:
            print("(tabla vacia todavia)")
        for dest, hop in sorted(next_hops.items()):
            print(f"  {dest} -> {hop}")
