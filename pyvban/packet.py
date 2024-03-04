import typing
from .const import *
from .subprotocols.audio import VBANAudioHeader
from .subprotocols.serial import VBANSerialHeader
from .subprotocols.text import VBANTextHeader


def parse_header(data: bytes) -> typing.Union[VBANAudioHeader, VBANSerialHeader, VBANTextHeader]:
    if len(data) != VBAN_HEADER_SIZE:
        raise Exception(f"Invalid header size provided expected {VBAN_HEADER_SIZE} got {len(data)}")

    if data[:4] != b"VBAN":
        raise Exception(f"Invalid fourcc in header expected b\"VBAN\" got {data[:4]}")

    sub_protocol = VBANProtocols(data[4] & VBAN_PROTOCOL_MASK)

    if sub_protocol == VBANProtocols.VBAN_PROTOCOL_AUDIO:
        return VBANAudioHeader.from_bytes(data)
    if sub_protocol == VBANProtocols.VBAN_PROTOCOL_SERIAL:
        return VBANSerialHeader.from_bytes(data)
    if sub_protocol == VBANProtocols.VBAN_PROTOCOL_TXT:
        return VBANTextHeader.from_bytes(data)
    # TODO: VBANProtocols.VBAN_PROTOCOL_SERVICE


class VBANPacket:
    def __init__(self, data: bytes):
        self._header = data[:VBAN_HEADER_SIZE]
        self._data = data[VBAN_HEADER_SIZE:]

        self._header_o = parse_header(self._header)

    def __repr__(self):
        return f"VBANPacket(proto={self._header_o.sub_protocol})"

    @property
    def header(self):
        return self._header_o

    @property
    def data(self):
        return self._data

