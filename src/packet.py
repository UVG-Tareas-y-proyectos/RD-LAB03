"""Construccion y lectura del paquete estandar del protocolo (ver enunciado 3.2)."""

import uuid


def build_packet(proto, ptype, src, dst, ttl, payload, headers=None):
    return {
        "proto": proto,
        "type": ptype,
        "from": src,
        "to": dst,
        "ttl": ttl,
        "headers": headers or [],
        "payload": payload,
    }


def new_message_id():
    return uuid.uuid4().hex


def get_header(packet, key):
    for header in packet.get("headers", []):
        if key in header:
            return header[key]
    return None


def with_header(packet, key, value):
    """Devuelve una copia del paquete con un header agregado (no muta el original)."""
    new_packet = dict(packet)
    new_packet["headers"] = list(packet.get("headers", [])) + [{key: value}]
    return new_packet
