import logging
import socket

from .. import VBANTextHeader
from ..const import VBAN_PROTOCOL_MAX_SIZE
from ..subprotocols.serial.const import VBANBaudRate, VBANSerialDataType
from ..subprotocols.text.const import VBANTextStreamType


class VBAN_SendText:
    def __init__(self, receiver_ip: str, receiver_port: int, stream_name: str):
        self._logger = logging.getLogger(f"VBAN_Sender_{receiver_ip}:{receiver_port}_{stream_name}")
        self._logger.info("Hellow world")

        self._receiver = (receiver_ip, receiver_port)
        self._stream_name = stream_name

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.connect(self._receiver)

        self._frame_counter = 0

        self._running = True

    def send(self, text: str):
        try:
            self._frame_counter += 1
            header = VBANTextHeader(
                baud_rate=VBANBaudRate.RATE_115200,
                channel=1,
                data_format=VBANSerialDataType.VBAN_SERIAL_DATA_TYPE_8BIT,
                text_type=VBANTextStreamType.VBAN_TEXT_STREAM_TYPE_ASCII,
                stream_name=self._stream_name,
                frame_counter=self._frame_counter,
            )

            data = header.to_bytes() + text.encode("utf-8")
            data = data[:VBAN_PROTOCOL_MAX_SIZE]
            self._socket.send(data)
        except Exception as e:
            self._logger.error(f"An exception occurred: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog='VBAN_SendText', description='Python based VBAN text sender')
    parser.add_argument('-a', '--address', required=True, type=str)
    parser.add_argument('-p', '--port', default=6980, type=int)
    parser.add_argument('-s', '--stream', default="Command1", type=str)
    parser.add_argument('text', type=str)
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    sender = VBAN_SendText(
        receiver_ip=args.address,
        receiver_port=args.port,
        stream_name=args.stream,
    )
    sender.send(args.text)
