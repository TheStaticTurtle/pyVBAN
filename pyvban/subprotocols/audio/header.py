import struct
from dataclasses import dataclass

from ...const import *
from .const import *


@dataclass
class VBANAudioHeader:
    sample_rate: VBANSampleRates
    samples_per_frame: int
    channels: int
    format: VBANBitResolution
    codec: VBANCodec
    stream_name: str
    frame_counter: int

    sub_protocol: VBANProtocols = VBANProtocols.VBAN_PROTOCOL_AUDIO

    @classmethod
    def from_bytes(cls, data: bytes):
        if len(data) != VBAN_HEADER_SIZE:
            raise Exception(f"Invalid header size provided expected {VBAN_HEADER_SIZE} got {len(data)}")

        if data[:4] != b"VBAN":
            raise Exception(f"Invalid fourcc in header expected b\"VBAN\" got {data[:4]}")

        proto = VBANProtocols(data[4] & VBAN_PROTOCOL_MASK)
        if proto != VBANProtocols.VBAN_PROTOCOL_AUDIO:
            raise Exception(f"Invalid sub protocol VBAN_PROTOCOL_AUDIO got {proto}")

        return VBANAudioHeader(
            sample_rate=VBANSampleRates(data[4] & VBAN_SR_MASK),
            samples_per_frame=data[5] + 1,
            channels=data[6] + 1,
            format=VBANBitResolution(data[7] & VBAN_BIT_RESOLUTION_MASK),
            codec=VBANCodec(data[7] & VBAN_CODEC_MASK),
            stream_name=b''.join(struct.unpack("cccccccccccccccc", data[8:24])).decode("utf-8").split('\x00', 1)[0],
            frame_counter=struct.unpack("<L", data[24:28])[0],
        )

    def to_bytes(self):
        header  = b"VBAN"
        header += bytes([self.sample_rate.value | VBANProtocols.VBAN_PROTOCOL_AUDIO.value])
        header += bytes([self.samples_per_frame - 1])
        header += bytes([self.channels - 1])
        header += bytes([self.format.value | self.codec.value])
        header += bytes(self.stream_name + "\x00" * (16 - len(self.stream_name)), 'utf-8')
        header += struct.pack("<L", self.frame_counter)
        return header

