"""Punto de entrada: levanta un nodo con el algoritmo que se le indique.

Uso:
    python -m src.main A --topo config/topo-example.txt \
        --addresses config/addresses-example.txt --algorithm lsr
"""

import argparse
import sys

from .config import load_addresses, load_topology
from .node import Node
from .routing.dijkstra import DijkstraStatic
from .routing.dvr import DVR
from .routing.flooding import Flooding
from .routing.lsr import LSR


def build_algorithm(name, node_id, neighbors, full_topology):
    if name == "flooding":
        return Flooding(node_id, neighbors)
    if name == "lsr":
        return LSR(node_id, neighbors)
    if name == "dvr":
        return DVR(node_id, neighbors)
    if name == "dijkstra":
        return DijkstraStatic(node_id, neighbors, full_topology)
    raise ValueError(f"algoritmo desconocido: {name}")


def main():
    parser = argparse.ArgumentParser(description="Levanta un nodo de la red")
    parser.add_argument("node_id")
    parser.add_argument("--topo", required=True)
    parser.add_argument("--addresses", required=True)
    parser.add_argument("--algorithm", required=True, choices=["flooding", "lsr", "dvr", "dijkstra"])
    args = parser.parse_args()

    topology = load_topology(args.topo)
    addresses = load_addresses(args.addresses)

    if args.node_id not in topology:
        sys.exit(f"el nodo {args.node_id} no esta en la topologia")
    if args.node_id not in addresses:
        sys.exit(f"el nodo {args.node_id} no tiene direccion asignada")

    neighbors = topology[args.node_id]
    algorithm = build_algorithm(args.algorithm, args.node_id, neighbors, topology)
    host, port = addresses[args.node_id]

    node = Node(args.node_id, host, port, neighbors, addresses, algorithm, args.algorithm)
    node.start()

    print(f"nodo {args.node_id} arriba en {host}:{port}, algoritmo={args.algorithm}, vecinos={neighbors}")
    print("comandos: send <destino> <mensaje> | table | quit")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if line == "quit":
            break
        if line == "table":
            node.print_table()
            continue
        if line.startswith("send "):
            parts = line.split(" ", 2)
            if len(parts) < 3:
                print("uso: send <destino> <mensaje>")
                continue
            _, dest, text = parts
            node.send_message(dest, text)
            continue
        print("comando no reconocido")


if __name__ == "__main__":
    main()
