"""
Copyright (C) 2011 Wagner Sartori Junior <wsartori@gmail.com>
http://www.wsartori.com

This file is part of txXBee.

txXBee program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from xbee.zigbee import ZigBee
from xbee.base import XBeeBase
from xbee.frame import APIFrame

from twisted.protocols.basic import LineReceiver

class txXBee(LineReceiver, ZigBee):
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
