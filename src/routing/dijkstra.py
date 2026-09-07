"""Dijkstra puro: se puede correr solo (con la topologia completa) o dentro de LSR."""

import heapq

from .base import RoutingAlgorithm


def shortest_paths(graph, source):
    """graph: {nodo: {vecino: costo}}. Devuelve (distancias, primer_salto_desde_source)."""
    dist = {source: 0}
    first_hop = {}
    visited = set()
    heap = [(0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        for v, cost in graph.get(u, {}).items():
            new_dist = d + cost
            if new_dist < dist.get(v, float("inf")):
                dist[v] = new_dist
                first_hop[v] = v if u == source else first_hop[u]
                heapq.heappush(heap, (new_dist, v))

    return dist, first_hop


class DijkstraStatic(RoutingAlgorithm):
    """Modo standalone: usa la topologia completa directo, sin descubrimiento dinamico.
    Es la excepcion que permite el enunciado (seccion 5, Anexo).
    """

    def __init__(self, node_id, neighbors, full_topology):
        super().__init__(node_id, neighbors)
        graph = {n: {nb: 1 for nb in nbs} for n, nbs in full_topology.items()}
        self.dist, self.next_hops = shortest_paths(graph, node_id)

    def next_hop(self, dest):
        return self.next_hops.get(dest)
