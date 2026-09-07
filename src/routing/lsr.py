"""Link State Routing: cada nodo manda su LSP a toda la red (via flooding) y
corre Dijkstra sobre la base de datos de enlaces que arma con lo que recibe.
"""

from .base import RoutingAlgorithm
from .dijkstra import shortest_paths


class LSR(RoutingAlgorithm):
    floods_info = True

    def __init__(self, node_id, neighbors):
        super().__init__(node_id, neighbors)
        # ponytail: costo fijo en 1, se podria medir con el RTT del hello
        self.link_costs = {n: 1 for n in neighbors}
        self.seq = 0
        self.lsdb = {node_id: {"neighbors": dict(self.link_costs), "seq": 0}}
        self.next_hops = {}

    def build_info_payloads(self):
        self.seq += 1
        self.lsdb[self.node_id] = {"neighbors": dict(self.link_costs), "seq": self.seq}
        return [{"source": self.node_id, "seq": self.seq, "neighbors": self.link_costs}]

    def on_info(self, packet, from_neighbor):
        payload = packet["payload"]
        source = payload["source"]
        seq = payload["seq"]

        known = self.lsdb.get(source)
        if known and known["seq"] >= seq:
            return False  # LSP viejo o repetido, no hay nada nuevo que propagar

        self.lsdb[source] = {"neighbors": payload["neighbors"], "seq": seq}
        self._recompute()
        return True

    def _recompute(self):
        graph = {n: info["neighbors"] for n, info in self.lsdb.items()}
        _, self.next_hops = shortest_paths(graph, self.node_id)

    def next_hop(self, dest):
        return self.next_hops.get(dest)
