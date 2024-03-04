import struct
from dataclasses import dataclass

from ...const import *
from .const import *
from ..serial.const import *


@dataclass
class VBANTextHeader:
    baud_rate: VBANBaudRate
    channel: int
    data_format: VBANSerialDataType
    text_type: VBANTextStreamType
    stream_name: str
    frame_counter: int

    sub_protocol: VBANProtocols = VBANProtocols.VBAN_PROTOCOL_TXT

    @classmethod
    def from_bytes(cls, data: bytes):
        if len(data) != VBAN_HEADER_SIZE:
            raise Exception(f"Invalid header size provided expected {VBAN_HEADER_SIZE} got {len(data)}")

        if data[:4] != b"VBAN":
            raise Exception(f"Invalid fourcc in header expected b\"VBAN\" got {data[:4]}")
        
        proto = VBANProtocols(data[4] & VBAN_PROTOCOL_MASK)
        if proto != VBANProtocols.VBAN_PROTOCOL_TXT:
            raise Exception(f"Invalid sub protocol VBAN_PROTOCOL_TXT got {proto}")

        if data[5] != 0x00:
            raise Exception(f"Invalid, VBAN_PROTOCOL_TXT requires byte at offset 5 to be 0x00 got {hex(data[5])}")

        return VBANTextHeader(
            baud_rate=VBANBaudRate(data[4] & VBAN_BR_MASK),
            channel=data[6] + 1,
            data_format=VBANSerialDataType(data[7] & VBAN_SERIAL_DATA_TYPE_MASK),
            text_type=VBANTextStreamType(data[7] & VBAN_TEXT_STREAM_TYPE_MASK),
            stream_name=b''.join(struct.unpack("cccccccccccccccc", data[8:24])).decode("utf-8").split('\x00', 1)[0],
            frame_counter=struct.unpack("<L", data[24:28])[0],
        )

    def to_bytes(self):
        header  = b"VBAN"
        header += bytes([self.baud_rate.value | VBANProtocols.VBAN_PROTOCOL_TXT.value])
        header += bytes([0x00])
        header += bytes([self.channel - 1])
        header += bytes([self.data_format.value | self.text_type.value])
        header += bytes(self.stream_name + "\x00" * (16 - len(self.stream_name)), 'utf-8')
        header += struct.pack("<L", self.frame_counter)
        return header

