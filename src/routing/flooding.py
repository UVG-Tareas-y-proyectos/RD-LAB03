from .base import RoutingAlgorithm


def broadcast_targets(neighbors, exclude=None):
    return [n for n in neighbors if n != exclude]


class Flooding(RoutingAlgorithm):
    """No arma tabla de ruteo, simplemente manda a todos los vecinos menos por donde llego."""

    def get_forward_targets(self, dest, from_neighbor):
        return broadcast_targets(self.neighbors, from_neighbor)
