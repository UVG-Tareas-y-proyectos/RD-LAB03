"""Distance Vector Routing: cada nodo solo conoce su vector y el de sus vecinos
directos, y lo va actualizando con la formula de Bellman-Ford.
"""

from .base import RoutingAlgorithm


class DVR(RoutingAlgorithm):
    def __init__(self, node_id, neighbors):
        super().__init__(node_id, neighbors)
        # ponytail: costo fijo en 1, se podria medir con el RTT del hello
        self.link_costs = {n: 1 for n in neighbors}
        self.dist = {node_id: 0, **self.link_costs}
        self.next_hops = {n: n for n in neighbors}

    def build_info_payloads(self):
        return [dict(self.dist)]

    def on_info(self, packet, from_neighbor):
        cost_to_neighbor = self.link_costs.get(from_neighbor)
        if cost_to_neighbor is None:
            return False  # info de alguien que no es mi vecino directo, no aplica

        changed = False
        for dest, cost in packet["payload"].items():
            if dest == self.node_id:
                continue
            new_cost = cost_to_neighbor + cost
            if new_cost < self.dist.get(dest, float("inf")):
                self.dist[dest] = new_cost
                self.next_hops[dest] = from_neighbor
                changed = True
        return changed

    def next_hop(self, dest):
        return self.next_hops.get(dest)
