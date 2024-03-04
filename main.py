# import logging
# import time

# import pyvban

# logging.basicConfig(level=logging.DEBUG)

# pyvban.utils.device_list()

# receiver = pyvban.utils.VBAN_Receiver(
#     sender_ip="127.0.0.1",
#     stream_name="Stream1",
#     port=6980,
#     device_index=11
# )
# receiver.run()

# sender = pyvban.utils.VBAN_Sender(
#     receiver_ip="127.0.0.1",
#     receiver_port=6980,
#     stream_name="Stream1",
#     sample_rate=48000,
#     channels=2,
#     device_index=1
# )
# sender.run()

# send_text = pyvban.utils.VBAN_SendText(
#     receiver_ip="127.0.0.1",
#     receiver_port=6980,
#     stream_name="Command1"
# )
# state = False
# while True:
#     state = not state
#     if state:
#         send_text.send("Strip[5].Mute = 0")
#     else:
#         send_text.send("Strip[5].Mute = 1")
#     time.sleep(1)
