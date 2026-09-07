"""Carga de los archivos de configuracion: topologia, nombres y direcciones locales."""

import json


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_topology(path):
    """topo-*.txt: {"type": "topo", "config": {"A": ["B", "C"], ...}}"""
    return _load(path)["config"]


def load_names(path):
    """names-*.txt: {"type": "names", "config": {"A": "foo@bar.com", ...}}"""
    return _load(path)["config"]


def load_addresses(path):
    """addresses-*.txt: solo para pruebas locales por TCP, no es parte del protocolo oficial.
    {"type": "addresses", "config": {"A": "127.0.0.1:6001", ...}}
    """
    raw = _load(path)["config"]
    addresses = {}
    for node_id, hostport in raw.items():
        host, port = hostport.split(":")
        addresses[node_id] = (host, int(port))
    return addresses
