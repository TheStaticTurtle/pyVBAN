# pyVBAN
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyVBAN)](https://pypi.org/project/pyVBAN/)


Python implementation of the VBAN (VB Audio network) protocol

Original specifications here: https://www.vb-audio.com/Voicemeeter/VBANProtocol_Specifications.pdf 

Supported sub-protocols:
 - [x] Audio
 - [x] Serial **(To verify)**
 - [x] Text 
 - [ ] Service

As I'm currently not using VBAN nor VB-Audio products I have no plans to implement this further. 
I will do my best to maintain it!

For any feature request, the specs are open, feel free to open a PR 😀

## Using the built-in utilities
### List devices
```bash
$ python -m pyvban.utils.device_list
```
```python
import logging
import pyvban
logging.basicConfig(level=logging.DEBUG)
pyvban.utils.device_list()
```

### Receiver
```bash
$ python -m pyvban.utils.receiver --address 127.0.0.1 --port 6980 --stream Stream1 --device 11
```
```python
import logging
import pyvban
logging.basicConfig(level=logging.DEBUG)
receiver = pyvban.utils.VBAN_Receiver(
    sender_ip="127.0.0.1",
    stream_name="Stream1",
    port=6980,
    device_index=11
)
receiver.run()
```

### Sender
```bash
$ python -m pyvban.utils.sender --address 127.0.0.1 --port 6980 --stream Stream1 --rate 48000 --channels 2 --device 1
```
```python
import logging
import pyvban
logging.basicConfig(level=logging.DEBUG)
sender = pyvban.utils.VBAN_Sender(
    receiver_ip="127.0.0.1",
    receiver_port=6980,
    stream_name="Stream1",
    sample_rate=48000,
    channels=2,
    device_index=1
)
sender.run()
```

### Send text
```bash
$ python -m pyvban.utils.send_text --address 127.0.0.1 --port 6980 --stream Command1 "Strip[5].Mute = 0"
```
```python
import logging
import pyvban
import time
logging.basicConfig(level=logging.DEBUG)
send_text = pyvban.utils.VBAN_SendText(
    receiver_ip="127.0.0.1",
    receiver_port=6980,
    stream_name="Command1"
)
state = False
while True:
    state = not state
    if state:
        send_text.send("Strip[5].Mute = 0")
    else:
        send_text.send("Strip[5].Mute = 1")
    time.sleep(1)
```


## Craft a packet manually

```python
import pyvban

pcm_data = b""  # 128 sample stereo data
header = pyvban.VBANAudioHeader(
    sample_rate=pyvban.subprotocols.audio.VBANSampleRates.RATE_48000,
    samples_per_frame=128,
    channels=2,
    format=pyvban.subprotocols.audio.VBANBitResolution.VBAN_BITFMT_16_INT,
    codec=pyvban.subprotocols.audio.VBANCodec.VBAN_CODEC_PCM,
    stream_name="Stream1",
    frame_counter=0,
)

vban_packet = header.to_bytes() + pcm_data
vban_packet = vban_packet[:pyvban.const.VBAN_PROTOCOL_MAX_SIZE]
```

## Parse a packet manually
```python
import pyvban

def run_once(self):
    data, addr = socket.recvfrom(pyvban.const.VBAN_PROTOCOL_MAX_SIZE)
    packet = pyvban.VBANPacket(data)
    if packet.header:
        if packet.header.sub_protocol != pyvban.const.VBANProtocols.VBAN_PROTOCOL_AUDIO:
            print(f"Received non audio packet {packet}")
            return
        if packet.header.stream_name != self._stream_name:
            print(f"Unexpected stream name \"{packet.header.stream_name}\" != \"{self._stream_name}\"")
            return
        if addr[0] != self._sender_ip:
            print(f"Unexpected sender \"{addr[0]}\" != \"{self._sender_ip}\"")
            return
```
