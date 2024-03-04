import struct
from dataclasses import dataclass

from ...const import *
from .const import *


@dataclass
class VBANSerialHeader:
    baud_rate: VBANBaudRate
    stop_bit: VBANSerialStopBit
    start_bit: VBANSerialStartBit
    parity: VBANSerialParityCheck
    multipart: bool
    channel: int
    data_format: VBANSerialDataType
    serial_type: VBANSerialStreamType
    stream_name: str
    frame_counter: int

    sub_protocol: VBANProtocols = VBANProtocols.VBAN_PROTOCOL_SERIAL

    @classmethod
    def from_bytes(cls, data: bytes):
        if len(data) != VBAN_HEADER_SIZE:
            raise Exception(f"Invalid header size provided expected {VBAN_HEADER_SIZE} got {len(data)}")

        if data[:4] != b"VBAN":
            raise Exception(f"Invalid fourcc in header expected b\"VBAN\" got {data[:4]}")
        
        proto = VBANProtocols(data[4] & VBAN_PROTOCOL_MASK)
        if proto != VBANProtocols.VBAN_PROTOCOL_SERIAL:
            raise Exception(f"Invalid sub protocol VBAN_PROTOCOL_SERIAL got {proto}")

        return VBANSerialHeader(
            baud_rate=VBANBaudRate(data[4] & VBAN_BR_MASK),
            stop_bit=VBANSerialStopBit(data[5] & VBAN_SERIAL_STOP_BIT_MASK),
            start_bit=VBANSerialStartBit((data[5] & VBAN_SERIAL_START_BIT_MASK) >> VBAN_SERIAL_START_BIT_SHIFT),
            parity=VBANSerialParityCheck((data[5] & VBAN_SERIAL_PARITY_CHECK_MASK) >> VBAN_SERIAL_PARITY_CHECK_SHIFT),
            multipart=data[5] & VBAN_SERIAL_MULTIPART_MASK,
            channel=data[6] + 1,
            data_format=VBANSerialDataType(data[7] & VBAN_SERIAL_DATA_TYPE_MASK),
            serial_type=VBANSerialStreamType(data[7] & VBAN_SERIAL_STREAM_TYPE_MASK),
            stream_name=b''.join(struct.unpack("cccccccccccccccc", data[8:24])).decode("utf-8").split('\x00', 1)[0],
            frame_counter=struct.unpack("<L", data[24:28])[0],
        )

    def to_bytes(self):
        header  = b"VBAN"
        header += bytes([self.baud_rate.value | VBANProtocols.VBAN_PROTOCOL_SERIAL.value])
        header += bytes([
            self.stop_bit.value |
            (self.start_bit.value << VBAN_SERIAL_START_BIT_SHIFT) |
            (self.parity.value << VBAN_SERIAL_PARITY_CHECK_SHIFT) |
            (0x80 if self.multipart else 0x00)
        ])
        header += bytes([self.channel - 1])
        header += bytes([self.data_format.value | self.serial_type.value])
        header += bytes(self.stream_name + "\x00" * (16 - len(self.stream_name)), 'utf-8')
        header += struct.pack("<L", self.frame_counter)
        return header

