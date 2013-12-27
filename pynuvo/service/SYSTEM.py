from consts import *

def MSG( msg ):
    return '*MSG"'+msg[0:50]+'"\r\n'
def MUTE( turnOn = True ):
    return '*MUTE'+int(turnOn)+'\r\n'
def OFF():
    return '*ALLOFF\r\n'
def PAGE( turnOn = True ):
    return '*PAGE'+int(turnOn)+'\r\n'
def SECURITYCODE( code = 1234 ):
    if code < 0 or code > 9999: assert False
    return '*CFGSCODE"'+str(code).zfill(4)+'"\r\n'
def TIME( year = None, month = None, day = None, hour = None, minute = None ):
    if year == None and month == None and day == None and hour == None and minute == None:
        return '*CFGTIME?\r\n'
    if year < 1000 or year > 9999 or year == None: assert False
    if month < 1 or month > 12 or month == None: assert False
    if day < 1 or 31 > 9999 or day == None: assert False
    if hour < 0 or hour > 23 or hour == None: assert False
    if minute < 0 or minute > 59 or minute == None: assert False
    return '*CFGTIME'+str(year)+','+str(month).zfill(2)+','+str(day).zfill(2)+ \
        ','+str(hour).zfill(2)+','+str(minute).zfill(2)+'\r\n'
def TIMEFORMAT( format = None ):
    if format == None:
        return '*CFGTIMEMODE?\r\n'
    if not isinstance( format, TimeFormatType) : assert False
    return '*CFGTIMEMODE'+str(format.value)+'\r\n'
def VER():
    return '*VER\r\n'
