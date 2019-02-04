import socket
import struct
import pyaudio


class VBAN_Recv(object):
	"""docstring for VBAN_Recv"""
	def __init__(self, senderIp, streamName, port, outDeviceIndex ,verbose=False):
		super(VBAN_Recv, self).__init__()
		self.streamName = streamName
		self.senderIp = senderIp
		self.const_VBAN_SRList = [6000, 12000, 24000, 48000, 96000, 192000, 384000, 8000, 16000, 32000, 64000, 128000, 256000, 512000,11025, 22050, 44100, 88200, 176400, 352800, 705600] 
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		self.sock.bind(("0.0.0.0", port))
		self.sampRate = 48000
		self.channels = 2
		self.outDeviceIndex=outDeviceIndex
		self.stream_magicString = ""
		self.stream_sampRate = 0
		self.stream_sampNum = 0
		self.stream_chanNum = 0
		self.stream_dataFormat = 0
		self.stream_streamName = ""
		self.stream_frameCounter = 0
		self.p = pyaudio.PyAudio()
		self.stream = self.p.open(format = self.p.get_format_from_width(2), channels = self.channels, rate = self.sampRate, output = True, output_device_index=self.outDeviceIndex)
		self.rawPcm = None
		self.running = True
		self.verbose = verbose
		self.rawData = None
		self.subprotocol = 0
		print("pyVBAN-Recv Started")
		print("Hint: Remeber that pyVBAN only support's PCM 16bits")

	def _correctPyAudioStream(self):
		self.channels = self.stream_chanNum 
		self.sampRate = self.stream_sampRate
		self.stream.close()
		self.stream = self.p.open(format = self.p.get_format_from_width(2), channels = self.channels, rate = self.sampRate, output = True, output_device_index=self.outDeviceIndex)

	def _cutAtNullByte(self,stri):
		return stri.split("\x00")[0]

	def _parseHeader(self,data):
		self.stream_magicString = data[0:4]
		sampRateIndex = ord(data[4]) & 0x1F
		self.subprotocol = (inByte & 0xE0) >> 5
		self.stream_sampRate = self.const_VBAN_SRList[sampRateIndex]
		self.stream_sampNum = ord(data[5]) + 1
		self.stream_chanNum = ord(data[6]) + 1
		self.stream_dataFormat = ord(data[7])
		self.stream_streamName = self._cutAtNullByte(''.join(struct.unpack("cccccccccccccccc",data[8:24])))
		self.stream_frameCounter = struct.unpack("l",data[24:28])[0]

	def runonce(self):
		if self.stream == None:
			print("Quit has been called")
			return
		data, addr = self.sock.recvfrom(2048) # buffer size is normally 1436 bytes Max size for vban
		self.rawData = data
		self._parseHeader(data)
		if self.verbose:
			print "R"+self.stream_magicString+" "+str(self.stream_sampRate)+"Hz "+str(self.stream_sampNum)+"samp "+str(self.stream_chanNum)+"chan Format:"+str(self.stream_dataFormat)+" Name:"+self.stream_streamName+" Frame:"+str(self.stream_frameCounter)
		self.rawPcm = data[28:]   #Header stops a 28
		if self.stream_magicString == "VBAN" and self.subprotocol == 0:
			if not self.stream_streamName == self.streamName:
				return
			if not addr[0] == self.senderIp:
				return
			if self.channels != self.stream_chanNum or self.sampRate != self.stream_sampRate:
				self._correctPyAudioStream()
			self.stream.write(self.rawPcm)

	def runforever(self):
		while self.running:
			self.runonce()
		self.quit()

	def quit(self):
		self.running = False
		self.stream.close()
		self.stream = None

class VBAN_Send(object):
	"""docstring for VBAN_Send"""
	def __init__(self, toIp, toPort, streamName, sampRate, inDeviceIndex ,verbose=False ):
		super(VBAN_Send, self).__init__()
		self.toIp = toIp
		self.toPort = toPort
		self.streamName = streamName
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		self.sock.connect((self.toIp,self.toPort))
		self.const_VBAN_SR = [6000, 12000, 24000, 48000, 96000, 192000, 384000, 8000, 16000, 32000, 64000, 128000, 256000, 512000,11025, 22050, 44100, 88200, 176400, 352800, 705600]
		self.p = pyaudio.PyAudio()
		self.channels = min([self.p.get_device_info_by_host_api_device_index(0, inDeviceIndex).get('maxInputChannels'),2])
		if sampRate not in self.const_VBAN_SR:
			print("SampRate not valid/compatible")
			return
		self.samprate = sampRate
		self.inDeviceIndex = inDeviceIndex
		self.chunkSize = 256
		self.stream = self.p.open(format=self.p.get_format_from_width(2), channels=self.channels,rate=self.samprate, input=True,input_device_index = self.inDeviceIndex, frames_per_buffer=self.chunkSize)
		self.framecounter = 0
		self.running = True
		self.verbose = verbose
		self.rawPcm = None
		self.rawData = None

	def _constructFrame(self,pcmData):
		header  = "VBAN" 
		header += chr(self.const_VBAN_SR.index(self.samprate))
		header += chr(self.chunkSize-1)
		header += chr(self.channels-1)
		header += chr(1)  #VBAN_CODEC_PCM
		header += self.streamName + "\x00" * (16 - len(self.streamName))
		header += struct.pack("l",self.framecounter)
		if self.verbose:
			print "SVBAN "+str(self.samprate)+"Hz "+str(self.chunkSize)+"samp "+str(self.channels)+"chan Format:1 Name:"+self.streamName+" Frame:"+str(self.framecounter)
		return header+pcmData

	def runonce(self):
		try:
			self.framecounter += 1
			self.rawPcm = self.stream.read(self.chunkSize)
			self.rawData = self._constructFrame(self.rawPcm)
			self.sock.sendto(self.rawData, (self.toIp,self.toPort))
		except:
			pass

	def runforever(self):
		while self.running:
			self.runonce()

	def quit(self):
		self.running = False
		self.stream.close()
		self.stream = None