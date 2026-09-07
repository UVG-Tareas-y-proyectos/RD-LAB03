"""Interfaz comun que usa el forwarding para tratar cualquier algoritmo igual."""


class RoutingAlgorithm:
    floods_info = False  # True si los paquetes info deben reenviarse a toda la red (LSR)

    def __init__(self, node_id, neighbors):
        self.node_id = node_id
        self.neighbors = neighbors

    def on_hello(self, packet, from_neighbor):
        pass

    def on_info(self, packet, from_neighbor):
        """Procesa un paquete tipo info. Devuelve True si cambio algo y debe reenviarse."""
        return False

    def build_info_payloads(self):
        """Que mandarle a los vecinos en la siguiente ronda de routing."""
        return []

    def next_hop(self, dest):
        return None

    def get_forward_targets(self, dest, from_neighbor):
        hop = self.next_hop(dest)
        return [hop] if hop else []
