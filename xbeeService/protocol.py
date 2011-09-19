from xbee.zigbee import ZigBee
from xbee.base import XBeeBase
from xbee.frame import APIFrame

from twisted.protocols.basic import LineReceiver

class ZigBeeProtocol(LineReceiver, ZigBee):
	def __init__(self, escaped=True):
		self._escaped = escaped
		self.frame = APIFrame(escaped=self._escaped)
		
		self.setRawMode()

	def rawDataReceived(self, data):
		if data[0] == APIFrame.START_BYTE:
			self.frame = APIFrame(escaped=self._escaped)
		for i in range(0, len(data)):
			self.frame.fill(data[i])
		if (not (self.frame.remaining_bytes() > 0)):
			try:
				# Try to parse and return result
				self.frame.parse()
				return getattr(self, "handle_packet", None)(self._split_response(self.frame.data))
			except ValueError:
				# Bad frame, so restart
				self.frame = APIFrame(escaped=self._escaped)

	def _write(self, data):
		frame = APIFrame(data, self._escaped).output()
		self.transport.write(frame)
