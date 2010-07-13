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
	Version = []
	Send = None
	def __init__(self, *args, **kwargs):
		ThreadedServer.__init__(self, *args, **kwargs)
		PyNuvoServer.Send = self._send
		self.con = Serial( 'COM1', 57600 )
		self.active = True
		self.thread_receive = threading.Thread(target = self.receive)
		self.thread_receive.start()
		#Do remaining initialization on Thread so that Windows service can start quicker
		self.thread_init = threading.Thread(target = self._bg_init)
		self.thread_init.start()
	def _bg_init(self):
		self._send( SYSTEM.VER() )
		for i in range(1, _MAX_ZONES+1):
			PyNuvoServer.Zones.append(PyNuvoService.exposed__Zone(i))
		for i in range(1, _MAX_SOURCES+1):
			PyNuvoServer.Sources.append(PyNuvoService.exposed__Source(i))
	def _send(self, cmd):
		self.con.write(cmd)
	def receive(self):
		while self.active:
			if self.con.inWaiting():
				self.handle_response( self.con.readline() )
			else:
				time.sleep(.5)
	def handle_response(self, msg):
		msg = msg.strip()
		if not msg[0:1] == '#': assert False
		elif msg[1:2] == '?': print 'Unknown'
		elif msg[1:7] == 'ALLOFF':
			for i in range(0, _MAX_ZONES):
				PyNuvoServer.Zones[i].exposed_status.exposed_power = False
		elif msg[1:2] == 'G':
			print msg
		elif msg[1:5] == 'MUTE':
			for i in range(0, _MAX_ZONES):
				if msg[5:6] == '1': PyNuvoServer.Zones[i].exposed_status.exposed_mute = True
				else: PyNuvoServer.Zones[i].exposed_status.exposed_mute = False				
		elif msg[1:3] == 'OK':
			pass
		elif msg[1:5] == 'PAGE':
			for i in range(0, _MAX_ZONES):
				if msg[5:6] == '1': PyNuvoServer.Zones[i].exposed_status.exposed_page = True
				else: PyNuvoServer.Zones[i].exposed_status.exposed_page = False	
		elif msg[1:5] == 'SCFG':
			source_num = int(msg[5:6]) - 1
			var = msg[7:].split(',')
			status = PyNuvoServer.Sources[source_num].exposed_status
			if var[0][6:7] == '0': 
				status.exposed_enable = False
			else: 
				status.exposed_enable = True
				status.exposed_name = var[1][5:-1]
				status.exposed_gain = int(var[2][4:])
				if var[3][7:8] == '1': status.exposed_nuvoNet = True
				else: status.exposed_nuvoNet = False
				status.exposed_shortname = var[4][10:-1]
		elif msg[1:2] == 'S':
			source_num = int(msg[2:3]) - 1
			if msg[3:9] == 'ACTIVE':
				status = PyNuvoServer.Sources[source_num].exposed_status
				if msg[9:10] == '1': status.exposed_nuvoNet = True
				else: status.exposed_nuvoNet = False
			elif msg[3:11] == 'DISPINFO':
				var = msg[12:].split(',')
				dispInfo = PyNuvoServer.Sources[source_num].exposed_dispInfo
				dispInfo.exposed_duration = int(var[0][3:])
				dispInfo.exposed_position = int(var[1][3:])
				dispInfo.exposed_status = int(var[2][6:])
			elif msg[3:11] == 'DISPLINE':
				line = int(msg[11:12])
				dispLine = PyNuvoServer.Sources[source_num].exposed_dispLine
				if line == 1: dispLine.exposed_line1= msg[13:-1]
				if line == 2: dispLine.exposed_line2= msg[13:-1]
				if line == 3: dispLine.exposed_line3= msg[13:-1]
				if line == 4: dispLine.exposed_line4= msg[13:-1]
			elif msg[3:7] == 'NAME':
				PyNuvoServer.Sources[source_num].exposed_status.exposed_name = msg[8:-1]
			else:
				print msg
				assert False
		elif msg[1:4] == 'VER':
			PyNuvoServer.Version = msg[5:-1].split()
		elif msg[1:4] == 'ZOS':
			print msg
		elif msg[1:5] == 'ZCFG':
			if msg[5:7].isdigit(): #Support up to 20 zones
				zone_num = int(msg[5:7]) - 1
				msg = msg[7:]
			else:
				zone_num = int(msg[5:6]) - 1
				msg = msg[6:]
			if msg[0:1] == ',':
				var = msg[1:].split(',')
				if var[0][0:4] == 'BASS':
					eq = PyNuvoServer.Zones[zone_num].exposed_eq
					eq.exposed_bass = int(var[0][4:])
					eq.exposed_treble = int(var[1][4:])
					if var[2][0:4] == 'BALC':
						eq.exposed_balance = 0
					elif var[2][0:4] == 'BALL':
						eq.exposed_balance = int(var[2][4:]) * -1
					else:
						eq.exposed_balance = int(var[2][4:])
					if var[3][7:8] == '1': eq.exposed_loudComp = True
					else: eq.exposed_loudComp = False
				elif var[0][0:6] == 'BRIGHT':
					disp = PyNuvoServer.Zones[zone_num].exposed_dispCfg
					disp.exposed_bright = int(var[0][6:7])
					disp.exposed_autodim = int(var[1][7:8])
					disp.exposed_dim = int(var[2][3:4])
					disp.exposed_dispMode = int(var[3][8:]) #Always 0: Not currently used
					if var[4][4:5] == '1': disp.exposed_time = True
					else: disp.exposed_time = False
				elif var[0][0:6] == 'ENABLE':
					config = PyNuvoServer.Zones[zone_num].exposed_config
					if var[0][6:7] == '0':
						config.exposed_enable = False
					elif var[0][6:7] == '1':
						config.exposed_enable = True
						config.exposed_name = var[1][5:-1]
						config.exposed_slaveTo = int(var[2][7:])
						config.exposed_group = int(var[3][5:])
						config.exposed_source1 = int(var[4][7:]) & (1<<0)
						config.exposed_source2 = int(var[4][7:]) & (1<<1)
						config.exposed_source3 = int(var[4][7:]) & (1<<2)
						config.exposed_source4 = int(var[4][7:]) & (1<<3)
						config.exposed_source5 = int(var[4][7:]) & (1<<4)
						config.exposed_source6 = int(var[4][7:]) & (1<<5)
						if var[5][4:5] == '1': config.exposed_xSrc = True
						else: config.exposed_xSrc = False
						config.exposed_ir = int(var[6][2:3])
						config.exposed_dndNoMute = int(var[7][3:4]) & (1<<0)
						config.exposed_dndNoPage = int(var[7][3:4]) & (1<<1)
						config.exposed_dndNoParty = int(var[7][3:4]) & (1<<2)
						if var[8][6:7] == '1': config.exposed_lock = True
						else: config.exposed_lock = False
				elif var[0][0:6] == 'MAXVOL':
					vol = PyNuvoServer.Zones[zone_num].exposed_volCfg
					vol.exposed_maxVol = int(var[0][6:])
					vol.exposed_initVol = int(var[1][6:])
					vol.exposed_pageVol = int(var[2][7:])
					vol.exposed_partyVol = int(var[3][8:])
					if var[4][6:7] == '1': vol.exposed_volReset = True
					else: vol.exposed_volReset = False
				else:
					assert False
						
		elif msg[1:2] == 'Z':
			if msg[2:4].isdigit(): #Support up to 20 zones
				zone_num = int(msg[2:4]) - 1
				msg = msg[4:]
			else:
				zone_num = int(msg[2:3]) - 1
				msg = msg[3:]
			if zone_num == -1:
				print 'IR control & Preset Macros still need to be implemented'
			elif msg[0:1] == ',':
				var = msg[1:].split(',')
				status = PyNuvoServer.Zones[zone_num].exposed_status
				if var[0] == 'OFF':
					status.exposed_power = False
				elif var[0] == 'ON':
					status.exposed_power = True
					status.exposed_source = int(var[1][3:])
					status.exposed_volume = int(var[2][3:])
					status.exposed_dnd = int(var[3][3:])
					status.exposed_lock = int(var[4][4:])
			elif msg[0:6] == 'ACTIVE':
				if msg[6:7] == '1': PyNuvoServer.Zones[zone_num].exposed_active = True
				else: PyNuvoServer.Zones[zone_num].exposed_active = False
			elif msg[0:8] == 'MENUITEM':
				##TODO Implement Zone Menu Item Functions
				print 'Need to Handle Zone Menu Items'
			elif msg[0:4] == 'MENU':
				##TODO Implement Zone Menu Functions
				print 'Need to Handle Zone Menus'
			elif msg[0:5] == 'PARTY':
				status = PyNuvoServer.Zones[zone_num].exposed_status
				if msg[5:6] == '1': status.exposed_partyHost = True
				else: status.exposed_partyHost = False
			elif msg[0:1] == 'S':
				source_num = int(msg[1:2]) - 1
				if msg[2:7] == 'IRCTL':
					macro_num = msg[7:]
					##TODO: Send notification of IR Control button
					print 'Need to Send notification of IR Control button'
				elif msg[2:7] == 'IRPRE':
					macro_num = msg[7:]
					##TODO: Send notification of IR Preset button
					print 'Need to Send notification of IR Preset button'
				elif msg[2:7] == 'MACRO':
					macro_num = msg[7:]
					##TODO: Send notification of Macro button
					print 'Need to Send notification of Macro button'
				elif msg[2:6] == 'NEXT':
					##TODO: Send notification of Next button
					print 'Need to Send notification of Next button'
				elif msg[2:11] == 'PLAYPAUSE':
					##TODO: Send notification of Play/Pause button
					print 'Need to Send notification of Play/Pause button'
				elif msg[2:6] == 'PREV':
					##TODO: Send notification of Previous button
					print 'Need to Send notification of Previous button'
				else:
					print msg
					assert False
			else:
				print msg
				assert False
		else:
			print msg
			assert False
		
class PyNuvoService(rpyc.Service):
	ALIASES = ["PyNuvo"]
	def __init__(self, conn):
		print 'pyNuvoService.__init__'
		rpyc.Service.__init__(self, conn)
		self.exposed_Version = PyNuvoServer.Version
	def on_connect(self):
		pass
	def on_disconnect(self):
		pass
	def exposed_Zone(self, index):
		if index not in range(1, _MAX_ZONES+1): assert False
		return PyNuvoServer.Zones[index-1]
	def exposed_Source(self, index):
		if index not in range(1, _MAX_SOURCES+1): assert False
		return PyNuvoServer.Sources[index-1]
	def exposed_Send(self, cmd):
		PyNuvoServer.Send( cmd )		
	class exposed__Zone:
		def __init__(self, num):
			self.exposed_number = num
			self.exposed_active = False
			PyNuvoServer.Send( ZONE.ACTIVE(num) ) # Fill Active State
			self.exposed_config = exposed__ZConfig()
			PyNuvoServer.Send( ZONE.CONFIG(num) ) # Fill config
			self.exposed_status = exposed__ZStatus()
			PyNuvoServer.Send( ZONE.STATUS(num) ) # Fill status
			self.exposed_eq = exposed__ZEQ()
			PyNuvoServer.Send( ZONE.EQ(num) ) # Fill EQ
			self.exposed_volCfg = exposed__ZVolCfg()
			PyNuvoServer.Send( ZONE.VOLCFG(num) ) # Fill Volume config
			self.exposed_dispCfg = exposed__ZDispCfg()
			PyNuvoServer.Send( ZONE.DISPCFG(num) ) # Fill Display config
	class exposed__Source:
		def __init__(self, num):
			self.exposed_number = num
			self.exposed_status = exposed__SStatus()
			PyNuvoServer.Send( SOURCE.CONFIG(num) ) # Fill status
			self.exposed_dispInfo = exposed__SDispInfo()
			PyNuvoServer.Send( SOURCE.DISPINFO(num) ) # Fill dispInfo
			self.exposed_dispLine = exposed__SDispLine()
			PyNuvoServer.Send( SOURCE.DISPLINE(num) ) # Fill dispLine
			
class exposed__SDispInfo:
	def __init__(self):
		self.exposed_duration = None
		self.exposed_position = None
		self.exposed_status = None
class exposed__SDispLine:
	def __init__(self):
		self.exposed_line1 = None
		self.exposed_line2 = None
		self.exposed_line3 = None
		self.exposed_line4 = None
class exposed__SStatus:
	def __init__(self):
		self.exposed_enable = None
		self.exposed_name = None
		self.exposed_gain = None
		self.exposed_nuvoNet = False
		self.exposed_shortname = None
class exposed__ZConfig:
	def __init__(self):
		self.exposed_enable = None
		self.exposed_name = None
		self.exposed_slaveTo = None
		self.exposed_group = None
		self.exposed_source1 = None
		self.exposed_source2 = None
		self.exposed_source3 = None
		self.exposed_source4 = None
		self.exposed_source5 = None
		self.exposed_source6 = None
		self.exposed_xSrc = None
		self.exposed_ir = None
		self.exposed_dndNoMute = None
		self.exposed_dndNoPage = None
		self.exposed_dndNoParty = None
		self.exposed_lock = None
class exposed__ZDispCfg:
	def __init__(self):
		self.exposed_bright = None
		self.exposed_autodim = None
		self.exposed_dim = None
		self.exposed_dispMode = None
		self.exposed_time = None
class exposed__ZEQ:
	def __init__(self):
		self.exposed_balance = None
		self.exposed_bass = None
		self.exposed_treble = None
		self.exposed_loudComp = None
class exposed__ZStatus:
	def __init__(self):
		self.exposed_power = None
		self.exposed_source = None
		self.exposed_volume = None
		self.exposed_mute = False
		self.exposed_dnd = None
		self.exposed_lock = None
		self.exposed_page = False
		self.exposed_partyHost = False
class exposed__ZVolCfg:
	def __init__(self):
		self.exposed_maxVol = None
		self.exposed_initVol = None
		self.exposed_pageVol = None
		self.exposed_partyVol = None
		self.exposed_volReset = None
		
if __name__ == '__main__':
	_spam = PyNuvoServer( PyNuvoService, port=16886 )
	_spam.start()
	while True:
		pass
		