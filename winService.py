import win32serviceutil
import win32service
import win32event
import win32api
from server import PyNuvoServer, PyNuvoService

class PyNuvoWin32(win32serviceutil.ServiceFramework):
	_svc_name_ = 'pyNuvoWin32'
	_svc_display_name_ = 'PyNuvo'
	def __init__(self, *args):
		win32serviceutil.ServiceFramework.__init__(self, *args)
		self.stop_event = win32event.CreateEvent(None, 0, 0, None)
	def log(self, msg):
		import servicemanager
		servicemanager.LogInfoMsg(str(msg))
	def SvcDoRun(self):
		self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
		try:
			self.ReportServiceStatus(win32service.SERVICE_RUNNING)
			self.start()
			win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
		except Exception, x:
			self.log('Exception : %s' % x)
			self.SvcStop()
	def SvcStop(self):
		self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
		self.stop()
		win32event.SetEvent(self.stop_event)
		self.ReportServiceStatus(win32service.SERVICE_STOPPED)
	# to be overridden
	def start(self): 
		self.server = PyNuvoServer( PyNuvoService, port = 16886 )
		self.server.start()
	def stop(self): 
		self.server.close()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(PyNuvoWin32)
