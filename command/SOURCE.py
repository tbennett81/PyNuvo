from consts import *

def ACTIVE( source ):
	return '*S'+str(source)+'ACTIVE?\r\n'
def CONFIG( source, enable = None, name = None, gain = None, shortname = None, nuvonet = None ):
	retval = ''
	if enable == None and name == None and gain == None and shortname == None and nuvonet == None:
		retval += '*SCFG'+str(source)+'STATUS?\r\n'
	else:
		if enable != None:
			if enable not in range(0,2): assert False
			retval += '*SCFG'+str(source)+'ENABLE'+str(enable)+'\r\n'
		if name != None:
			retval += '*SCFG'+str(source)+'NAME"'+name[0:20]+'"\r\n'
		if gain != None:
			if gain not in range(0,15): assert False
			retval += '*SCFG'+str(source)+'GAIN'+str(gain)+'\r\n'
		if shortname != None:
			retval += '*SCFG'+str(source)+'SHORTNAME"'+shortname[0:3]+'"\r\n'
		if nuvonet != None:
			if nuvonet not in range(0,2): assert False
			retval += '*SCFG'+str(source)+'NUVONET'+str(nuvonet)+'\r\n'
	return retval
def DISPINFO( source, totalTime = None, currentTime = None, status = None ):
	if totalTime == None or currentTime == None or status == None:
		return '*S'+str(source)+'DISPINFO?\r\n'
	if status not in range(0,9): assert False
	return '*S'+str(source)+'DISPINFO,'+str(totalTime)+','+str(currentTime)+','+str(status)+'\r\n'		
def DISPLINE( source, line1 = None, line2 = None, line3 = None, line4 = None ):
	retval = ''
	if line1 == None and line2 == None and line3 == None and line4 == None: 
		retval += '*S'+str(source)+'DISPLINE?\r\n'
	else:
		if line1 != None:
			retval += '*S'+str(source)+'DISPLINE1"'+line1+'"\r\n'
		if line2 != None:
			retval += '*S'+str(source)+'DISPLINE2"'+line2+'"\r\n'
		if line3 != None:
			retval += '*S'+str(source)+'DISPLINE3"'+line3+'"\r\n'
		if line4 != None:
			retval += '*S'+str(source)+'DISPLINE4"'+line4+'"\r\n'
	return retval
def MSG( source, msg, msg_type = INFORMATION, msg_time = NORMAL ):
	if msg_type not in range(0,4): assert False
	if msg_time not in range(0,3): assert False
	return '*S'+str(source)+'MSG"'+msg[0:20]+'",'+str(msg_type)+','+str(msg_time)+'\r\n'
def NAME( source, name = None ):
	if name == None:
		return '*S'+str(source)+'NAME?\r\n'
	else:
		return '*S'+str(source)+'NAME"'+name+'"\r\n'
