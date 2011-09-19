from twisted.python import log, usage
from twisted.internet import reactor, task
from twisted.internet.serialport import SerialPort
from twisted.web.http_headers import Headers

from struct import unpack

import sys

from xbeeService.protocol import ZigBeeProtocol

class MyOptions(usage.Options):
	optParameters = [
		['outfile', 'o', None, 'Logfile [default: sys.stdout]'],
		['baudrate', 'b', 38400, 'Serial baudrate [default: 38400'],
		['port', 'p', '/dev/tty.usbserial-A600ezgH', 'Serial Port device'],
	]

devices = {
	"template": "\x00\x13\xA2\x00\x00\x00\x00\x00",
	"template1": "\x00\x13\xA2\x00\x00\x00\x00\x00",
	"template2": "\x00\x13\xA2\x00\x00\x00\x00\x00",
}

class YourWrapperName(ZigBeeProtocol):
	def __init__(self, *args, **kwds):
		super(YourWrapperName, self).__init__(*args, **kwds)
		self.lc = task.LoopingCall(self.getSomeData)
		self.lc.start(30.0)

	def handle_packet(self, xbeePacketDictionary):
		response = xbeePacketDictionary
		if response.get("source_addr_long", "default") == devices["template1"]:
			reactor.callFromThread(self.send,
			          "tx",
			          frame_id="\x01",
			          dest_addr_long=devices["template1"],
			          dest_addr="\xff\xfe",
			          data="DATA1")
			reactor.callFromThread(self.send,
			         "tx",
			         frame_id="\x01",
			         dest_addr_long=devices["template2"],
			         dest_addr="\xff\xfe",
			         data="DATA2")

	def getSomeData(self):
		reactor.callFromThread(self.send,
		             "tx",
		             frame_id="\x01",
		             dest_addr_long=devices["template1"],
		             dest_addr="\xff\xfe",
		             data="SEND_ME_SOME_DATA")

if __name__ == '__main__':
	o = MyOptions()
	try:
		o.parseOptions()
	except usage.UsageError, errortext:
		print '%s: %s' % (sys.argv[0], errortext)
		print '%s: Try --help for usage details.' % (sys.argv[0])
		raise SystemExit, 1

	logFile = o.opts['outfile']
	if logFile is None:
		logFile = sys.stdout
	log.startLogging(logFile)

	port = o.opts['port']
	log.msg('Attempting to open %s at %dbps as a %s device' % (port, o.opts['baudrate'], ZigBeeProtocol.__name__))
	
	s = SerialPort(YourWrapperName(escaped=True), o.opts['port'], reactor, baudrate=o.opts['baudrate'])
	
	reactor.run()
