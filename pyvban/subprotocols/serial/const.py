import enum

VBAN_BR_MASK      = 0x1F
class VBANBaudRate(enum.Enum):
    RATE_0       = 0
    RATE_110     = 1
    RATE_150     = 2
    RATE_300     = 3
    RATE_600     = 4
    RATE_1200    = 5
    RATE_2400    = 6
    RATE_4800    = 7
    RATE_9600    = 8
    RATE_14400   = 9
    RATE_19200   = 10
    RATE_31250   = 11
    RATE_38400   = 12
    RATE_57600   = 13
    RATE_115200  = 14
    RATE_128000  = 15
    RATE_230400  = 16
    RATE_250000  = 17
    RATE_256000  = 18
    RATE_460800  = 19
    RATE_921600  = 20
    RATE_1000000  = 21
    RATE_1500000  = 22
    RATE_2000000  = 23
    RATE_3000000  = 24
    RATE_UNDEFINED1 = 25
    RATE_UNDEFINED2 = 26
    RATE_UNDEFINED3 = 27
    RATE_UNDEFINED4 = 28
    RATE_UNDEFINED5 = 29
    RATE_UNDEFINED6 = 30
    RATE_UNDEFINED7 = 31

VBAN_SERIAL_STOP_BIT_MASK = 0x03
class VBANSerialStopBit(enum.Enum):
    VBAN_SERIAL_1_END_BIT     = 0
    VBAN_SERIAL_1_5_END_BIT   = 1
    VBAN_SERIAL_2_END_BIT     = 2
    VBAN_SERIAL_NO_END_BIT    = 3

VBAN_SERIAL_START_BIT_MASK = 0x04
VBAN_SERIAL_START_BIT_SHIFT = 2
class VBANSerialStartBit(enum.Enum):
    VBAN_SERIAL_1_START_BIT   = 0
    VBAN_SERIAL_NO_START_BIT  = 1

VBAN_SERIAL_PARITY_CHECK_MASK = 0x08
VBAN_SERIAL_PARITY_CHECK_SHIFT = 3
class VBANSerialParityCheck(enum.Enum):
    VBAN_SERIAL_NO_PARITY_CHECK = 0
    VBAN_SERIAL_PARITY_CHECK    = 1

VBAN_SERIAL_MULTIPART_MASK = 0x80


VBAN_SERIAL_DATA_TYPE_MASK = 0x07
class VBANSerialDataType(enum.Enum):
    VBAN_SERIAL_DATA_TYPE_8BIT       = 0
    VBAN_SERIAL_DATA_TYPE_UNDEFINED1 = 1
    VBAN_SERIAL_DATA_TYPE_UNDEFINED2 = 2
    VBAN_SERIAL_DATA_TYPE_UNDEFINED3 = 3
    VBAN_SERIAL_DATA_TYPE_UNDEFINED4 = 4
    VBAN_SERIAL_DATA_TYPE_UNDEFINED5 = 5
    VBAN_SERIAL_DATA_TYPE_UNDEFINED6 = 6
    VBAN_SERIAL_DATA_TYPE_UNDEFINED7 = 7

VBAN_SERIAL_STREAM_TYPE_MASK = 0xF0
class VBANSerialStreamType(enum.Enum):
    VBAN_SERIAL_STREAM_TYPE_GENERIC     = 0x00
    VBAN_SERIAL_STREAM_TYPE_MIDI        = 0x10
    VBAN_SERIAL_STREAM_TYPE_UNDEFINED1  = 0x20
    VBAN_SERIAL_STREAM_TYPE_UNDEFINED2  = 0x30
    VBAN_SERIAL_STREAM_TYPE_UNDEFINED3  = 0x40
    VBAN_SERIAL_STREAM_TYPE_UNDEFINED4  = 0x50
    VBAN_SERIAL_STREAM_TYPE_UNDEFINED5  = 0x60
    VBAN_SERIAL_STREAM_TYPE_UNDEFINED6  = 0x70
    VBAN_SERIAL_STREAM_TYPE_UNDEFINED7  = 0x80
    VBAN_SERIAL_STREAM_TYPE_UNDEFINED9  = 0x90
    VBAN_SERIAL_STREAM_TYPE_UNDEFINED10 = 0xA0
    VBAN_SERIAL_STREAM_TYPE_UNDEFINED11 = 0xB0
    VBAN_SERIAL_STREAM_TYPE_UNDEFINED12 = 0xC0
    VBAN_SERIAL_STREAM_TYPE_UNDEFINED13 = 0xD0
    VBAN_SERIAL_STREAM_TYPE_UNDEFINED14 = 0xE0
    VBAN_SERIAL_STREAM_TYPE_USER        = 0xF0

