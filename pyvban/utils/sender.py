import logging
import socket

import pyaudio

from .. import VBANAudioHeader
from ..const import *
from ..subprotocols.audio.const import VBANSampleRatesSR2Enum, VBANBitResolution, VBANCodec


class VBAN_Sender:
    def __init__(self, receiver_ip: str, receiver_port: int, stream_name: str, sample_rate: int, channels: int, device_index: int):
        self._logger = logging.getLogger(f"VBAN_Sender_{receiver_ip}:{receiver_port}_{stream_name}")
        self._logger.info("Hellow world")

        self._receiver = (receiver_ip, receiver_port)
        self._stream_name = stream_name
        self._sample_rate = sample_rate
        self._vban_sample_rate = VBANSampleRatesSR2Enum[sample_rate]
        self._channels = channels
        self._device_index = device_index

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._samples_per_frame = 128

        self._p = pyaudio.PyAudio()
        self._stream = self._p.open(
            format=self._p.get_format_from_width(2),
            channels=self._channels,
            rate=self._sample_rate,
            input=True,
            input_device_index=self._device_index
        )

        self._frame_counter = 0

        self._running = True

    def run_once(self):
        try:
            self._frame_counter += 1
            header = VBANAudioHeader(
                sample_rate=self._vban_sample_rate,
                samples_per_frame=self._samples_per_frame,
                channels=self._channels,
                format=VBANBitResolution.VBAN_BITFMT_16_INT,
                codec=VBANCodec.VBAN_CODEC_PCM,
                stream_name=self._stream_name,
                frame_counter=self._frame_counter,
            )

            data = header.to_bytes() + self._stream.read(self._samples_per_frame)
            data = data[:VBAN_PROTOCOL_MAX_SIZE]

            self._socket.sendto(data, self._receiver)
        except Exception as e:
            self._logger.error(f"An exception occurred: {e}")

    def run(self):
        self._running = True
        while self._running:
            self.run_once()
        self.stop()

    def stop(self):
        self._running = False
        self._stream.close()
        self._stream = None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog='VBAN_Sender', description='Python based VBAN streamer')
    parser.add_argument('-a', '--address', required=True, type=str)
    parser.add_argument('-p', '--port', default=6980, type=int)
    parser.add_argument('-s', '--stream', default="Stream1", type=str)
    parser.add_argument('-r', '--rate', default=48000, type=int)
    parser.add_argument('-c', '--channels', default=2, type=int)
    parser.add_argument('-d', '--device', default=-1, required=True, type=int)
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    sender = VBAN_Sender(
        receiver_ip=args.address,
        receiver_port=args.port,
        stream_name=args.stream,
        sample_rate=args.rate,
        channels=args.channels,
        device_index=args.device
    )
    sender.run()
