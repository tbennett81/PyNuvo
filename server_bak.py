import rpyc
import threading
import time

from command import consts, SOURCE, SYSTEM, ZONE
#from Math import max, min
from serial import Serial
from rpyc.utils.server import ThreadedServer

_MAX_SOURCES = 6
_MAX_ZONES = 8

class PyNuvoServer(ThreadedServer):
	Zones = []
	Sources = []
	Version = ''
	Send = None
	def __init__(self, *args, **kwargs):
		print 'PyNuvoServer.__init__'
		ThreadedServer.__init__(self, *args, **kwargs)
		PyNuvoServer.Send = self._send
		self.con = Serial( 'COM1', 57600 )
		self.active = True
		self.thread = threading.Thread(target = self.receive)
		self.thread.start()
		self._send( SYSTEM.VER() )
		for i in range(1, _MAX_ZONES+1):
			PyNuvoServer.Zones.append(PyNuvoService.exposed__Zone(i, self._send))
		for i in range(1, _MAX_SOURCES+1):
			PyNuvoServer.Sources.append(PyNuvoService.exposed__Source(i, self._send))
	def _send(self, cmd):
		self.con.write(cmd)
	def receive(self):
		print 'Start receive'
		while self.active:
			if self.con.inWaiting():
				print self.con.readline()
			else:
				time.sleep(.5)
		
class PyNuvoService(rpyc.Service):
	ALIASES = ["PyNuvo"]
	def __init__(self, conn):
		print 'pyNuvoService.__init__'
		rpyc.Service.__init__(self, conn)
		self.exposed_Version = PyNuvoServer.Version
	def on_connect(self):
		print 'found someone'
	def on_disconnect(self):
		print 'lost someone'
	def exposed_Zone(self, index):
		if index not in range(1, _MAX_ZONES+1): assert False
		return PyNuvoServer.Zones[index-1]
	def exposed_Source(self, index):
		if index not in range(1, _MAX_SOURCES+1): assert False
		return PyNuvoServer.Sources[index-1]
	def exposed_Send(self, cmd):
		PyNuvoServer.Send( cmd )		
	class exposed__Zone:
		def __init__(self, num, send):
			self._number = num
			self._send = send
		def exposed_DoNotDisturb(self, turnOn = None):
			if turnOn != None and type(turnOn).__name__=='bool':
				self._DND = turnOn
				self._send( ZONE.DONOTDISTURB( self._number, self._DND ) )
			return self._DND
		def exposed_Msg(self, msg, type = consts.INFORMATION, time = consts.NORMAL):
			self._send( ZONE.MSG(self._number, msg, type, time) )
		def exposed_Mute(self, muteOn = None):
			if muteOn != None and type(muteOn).__name__=='bool':
				self._mute = muteOn
				self._send( ZONE.MUTE(self._number, self._mute) )
			return self._mute
		def exposed_Number(self):
			return self._number
		def exposed_Party(self, turnOn = None):
			if turnOn != None and type(turnOn).__name__=='bool':
				self._party = turnOn
				self._send( ZONE.PARTY(self._number, self._party) )
			return self._party
		def exposed_Power(self, powerOn = None):
			if powerOn != None and type(powerOn).__name__=='bool':
				self._power = powerOn
				self._send( ZONE.POWER(self._number, self._power) )
			return self._power
		def exposed_RawSend(self, msg):
			self._send( msg )
		def exposed_SimNext(self):
			self._send( ZONE.SIMNEXT(self._number) )
		def exposed_SimPlayPause(self):
			self._send( ZONE.SIMPLAYPAUSE(self._number) )
		def exposed_SimPrev(self):
			self._send( ZONE.SIMPREV(self._number) )
		def exposed_Source(self, source = None):
			if source != None and source in range(1, _MAX_SOURCES+1):
				self._source = source
				self._send( ZONE.SOURCE(self._number, self._source) )
			return self._source
		def exposed_SourceUp(self):
			self._source = (self._source % _MAX_SOURCES) + 1
			self._send( ZONE.NEXTSOURCE( self._number ) )
		def exposed_Volume(self, level = None ):
			if level != None and level in range(0,80):
				self._volume = level
				self._send( ZONE.VOLUME(self._number, self._volume) )
			return self._volume
		def exposed_VolumeUp(self):
			self._volume = min(self._volume+1, 79)
			self._send( ZONE.VOLUMEUP(self._number) )
			return self._volume
		def exposed_VolumeDn(self):
			self._volume = max(self._volume-1, 0)
			self._send( ZONE.VOLUMEDN(self._number) )
			return self._volume
	class exposed__Source:
		def __init__(self, num, send):
			self._number = num
			self._send = send
		def exposed_getNumber(self):
			return self._number
		
if __name__ == '__main__':
	_spam = PyNuvoServer( PyNuvoService, port=16886 )
	_spam.start()
	while True:
		pass
		