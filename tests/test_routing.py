"""Chequeo rapido de los algoritmos, sin frameworks. Correr con: python tests/test_routing.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import packet as pkt
from src.routing.dijkstra import shortest_paths
from src.routing.dvr import DVR
from src.routing.flooding import broadcast_targets
from src.routing.lsr import LSR

GRAPH = {
    "A": {"B": 1, "D": 1},
    "B": {"A": 1, "C": 1},
    "C": {"B": 1, "D": 1},
    "D": {"A": 1, "C": 1},
}


def test_dijkstra_shortest_path():
    dist, first_hop = shortest_paths(GRAPH, "A")
    assert dist["C"] == 2
    assert first_hop["C"] in ("B", "D")  # dos caminos igual de cortos, cualquiera vale


def test_flooding_excludes_sender():
    targets = broadcast_targets(["B", "C", "D"], exclude="B")
    assert targets == ["C", "D"]


def test_lsr_converges_to_full_graph():
    node = LSR("A", ["B", "D"])
    for src, neighbors in GRAPH.items():
        if src == "A":
            continue
        lsp = pkt.build_packet("lsr", "info", src, "A", 8, {"source": src, "seq": 1, "neighbors": neighbors})
        node.on_info(lsp, from_neighbor=None)
    assert node.next_hop("C") in ("B", "D")


def test_lsr_ignores_stale_lsp():
    node = LSR("A", ["B"])
    fresh = pkt.build_packet("lsr", "info", "C", "A", 8, {"source": "C", "seq": 5, "neighbors": {"B": 1}})
    stale = pkt.build_packet("lsr", "info", "C", "A", 8, {"source": "C", "seq": 2, "neighbors": {"B": 1}})
    assert node.on_info(fresh, from_neighbor="B") is True
    assert node.on_info(stale, from_neighbor="B") is False


def test_dvr_updates_via_neighbor():
    node = DVR("A", ["B"])
    vector = pkt.build_packet("dvr", "info", "B", "A", 8, {"B": 0, "C": 1})
    changed = node.on_info(vector, from_neighbor="B")
    assert changed is True
    assert node.dist["C"] == 2  # costo A-B (1) + B-C (1)
    assert node.next_hop("C") == "B"


def test_packet_headers():
    base = pkt.build_packet("dvr", "message", "A", "C", 5, "hola")
    with_hop = pkt.with_header(base, "hop", "B")
    assert pkt.get_header(with_hop, "hop") == "B"
    assert pkt.get_header(base, "hop") is None  # el original no se muta


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print(f"ok: {test.__name__}")
    print(f"\n{len(tests)} pruebas pasaron")
