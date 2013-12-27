from consts import *

def ACTIVE( zone ):
    return '*Z'+str(zone)+'ACTIVE?\r\n'
def CONFIG(zone, enable=None, name=None, slaveTo=None, group=None, sources=None, xsrc=None, ir=None, dnd=None, lock=None ):
    if enable==None and name==None and slaveTo==None and group==None and \
        sources==None and xsrc==None and ir==None and dnd==None and lock==None:
        return '*ZCFG'+str(zone)+'STATUS?\r\n'
    else:
        retval = ''
        if enable != None:
            retval += '*ZCFG'+str(zone)+'ENABLE'+str(int(enable))+'\r\n'
        if name != None:
            retval += '*ZCFG'+str(zone)+'NAME"'+name[0:20]+'"\r\n'
        if slaveTo != None:
            if slaveTo<1 or slaveto>16: assert False
            retval += '*ZCFG'+str(zone)+'SLAVETO'+str(slaveTo)+'\r\n'
        if group != None:
            if group<0 or group>4: assert False
            retval += '*ZCFG'+str(zone)+'GROUP'+str(group)+'\r\n'
        #Expects a bitmask of sources.  Use SOURCE to have bitmask created for you
        if sources != None:
            if sources<0 or sources>63: assert False
            retval += '*ZCFG'+str(zone)+'SOURCES'+str(sources)+'\r\n'
        if xsrc != None:
            retval += '*ZCFG'+str(zone)+'XSRC'+str(int(xsrc))+'\r\n'
        if ir != None:
            if not isinstance( ir, IRStateType ): assert False
            retval += '*ZCFG'+str(zone)+'IR'+str(ir.value)+'\r\n'
        #Expects a bitmask of DND State. Use DNDSTATE to have this created for you.
        if dnd != None:
            if dnd<0 or dnd>7: assert False
            retval += '*ZCFG'+str(zone)+'DND'+str(dnd)+'\r\n'
        if lock != None:
            retval += '*ZCFG'+str(zone)+'LOCKED'+str(int(lock))+'\r\n'
        return retval
def CFGDND( zone, noMute = True, noPage = True, noParty = True ):
    mask = (noMUTE<<0) | (noPage<<1) | (noParty<<2)
    return '*ZCFG'+str(zone)+'DND'+mask+'\r\n'
def DISPCFG( zone, bright=None, autoDim=None, dim=None, dispMode=None, time=None ):
    if bright==None and autoDim==None and dim==None and dispMode==None and time==None:
        return '*ZCFG'+str(zone)+'DISP?\r\n'
    else:
        retval = ''
        if bright != None:
            retval += '*ZCFG'+str(zone)+'BRIGHT'+str(bright)+'\r\n'
        if autoDim != None:
            retval += '*ZCFG'+str(zone)+'AUTODIM'+str(autoDim)+'\r\n'
        if dim != None:
            retval += '*ZCFG'+str(zone)+'DIM'+str(dim)+'\r\n'
        if dispMode != None:
            retval += '*ZCFG'+str(zone)+'DISPMODE0\r\n' #Not currently supported
        if time != None:
            retval += '*ZCFG'+str(zone)+'TIME'+str(int(time))+'\r\n'
        return retval
def DND( zone, turnOn ):
    if turnOn:
        return '*Z'+str(zone)+'DNDON\r\n'
    else:
        return '*Z'+str(zone)+'DNDOFF\r\n'
def EQ( zone, bal=None, bass=None, treb=None, comp=None ):
    if bal==None and bass==None and treb==None and comp==None:
        return '*ZCFG'+str(zone)+'EQ?\r\n'
    else:
        retval = ''
        if bal != None:
            if bal not in range(-18,19,2): assert False
            elif bal < 0: retval += '*ZCFG'+str(zone)+'BALL'+str(abs(bal))+'\r\n'
            elif bal > 0: retval += '*ZCFG'+str(zone)+'BALR'+str(bal)+'\r\n'
            else: retval += '*ZCFG'+str(zone)+'BALC\r\n'
        if bass != None:
            if bass not in range(-18,19,2): assert False
            retval += '*ZCFG'+str(zone)+'BASS'+str(bass)+'\r\n'
        if treb != None:
            if treb not in range(-18,19,2): assert False
            retval += '*ZCFG'+str(zone)+'TREB'+treb+'\r\n'
        if comp != None:
            retval += '*ZCFG'+str(zone)+'LOUDCMP'+str(int(comp))+'\r\n'
        return retval
def FAVORITE( zone, fav ):
    if fav<1 or fav>12: assert False
    return '*Z'+str(zone)+'FAV'+str(fav)+'\r\n'
def IRCONTROLMACRO( zone, macro ):
    return '*Z'+str(zone)+'IRCTL'+str(macro)+'\r\n'
def IRPRESETMACRO( zone, macro ):
    return '*Z'+str(zone)+'IRPRE'+str(macro)+'\r\n'
def LOCK( zone, turnOn, passcode = None ):
    if turnOn:
        return '*Z'+str(zone)+'LOCKON\r\n'
    else:
        if passcode == None: assert False
        return '*Z'+str(zone)+'LOCKOFF"'+str(passcode).zfill(4)+'"\r\n'
def MSG( zone, msg, msg_type = MessageType.Information, msg_time = MsgTimeType.Normal ):
    if not isinstance(msg_type, MessageType): assert False
    if not isinstance(msg_time, MsgTimeType): assert False
    return '*Z'+str(zone)+'MSG"'+msg[0:20]+'",'+str(msg_type.value)+','+str(msg_time.value)+'\r\n'
def MUTE( zone, turnOn ):
    if turnOn:
        return '*Z'+str(zone)+'MUTEON\r\n'
    else:
        return '*Z'+str(zone)+'MUTEOFF\r\n'
def NEXTSOURCE( zone ):
    return '*Z'+str(zone)+'SRC+\r\n'
def PARTY( zone, turnOn ):
    return '*Z'+str(zone)+'PARTY'+int(turnOn)+'\r\n'
def POWER( zone, turnOn ):
    if turnOn:
        return '*Z'+str(zone)+'ON\r\n'
    else:
        return '*Z'+str(zone)+'OFF\r\n'
def SERIALREDIRECT( zone, redirect ):
    #UNTESTED
    return '*Z'+str(zone)+'SERIAL'+int(redirect)+'\r\n'
def SIM( zone, button, action, menuid, itemid, itemindex ):
    #UNTESTED
    if button<1 or button>8: assert False
    if action<0 or action>2: assert False
    return '*Z'+str(zone)+'BUTTON'+str(button)+','+str(action)+','+ \
        str(menuid)+','+str(itemid)+','+str(itemindex)
def SIMNEXT( zone ):
    return '*Z'+str(zone)+'NEXT\r\n' 
def SIMPLAYPAUSE( zone ):
    return '*Z'+str(zone)+'PLAYPAUSE\r\n' 
def SIMPREV( zone ):
    return '*Z'+str(zone)+'PREV\r\n' 
def SOURCE( zone, source ):
    return '*Z'+str(zone)+'SRC'+str(source)+'\r\n'
def SOURCEENABLE( zone, src1 = True, src2 = True, src3 = True, src4 = True, src5 = True, src6 = True ):
    sources = (src1 << 0) | (src2 << 1) | (src3 << 2) | (src4 << 3) | (src5 << 4) | (src6 << 5)
    return '*ZCFG'+str(zone)+'SOURCES'+str(sources)+'\r\n'
def STATUS( zone ):
    return '*Z'+str(zone)+'STATUS?\r\n'
def VOLCFG( zone, max=None, initial=None, page=None, party=None, reset=None ):
    if max==None and initial==None and page==None and party==None and reset==None:
        return '*ZCFG'+str(zone)+'VOL?\r\n'
    else:
        retval = ''
        if max != None:
            if max<0 or max>79: assert False
            retval += '*ZCFG'+str(zone)+'MAXVOL'+str(max)+'\r\n'
        if initial != None:
            if initial<0 or initial>79: assert False
            retval += '*ZCFG'+str(zone)+'INIVOL'+str(initial)+'\r\n'
        if page != None:
            if page<0 or page>79: assert False
            retval += '*ZCFG'+str(zone)+'PAGEVOL'+str(page)+'\r\n'
        if party != None:
            if party<0 or party>79: assert False
            retval += '*ZCFG'+str(zone)+'PARTYVOL'+str(party)+'\r\n'
        if reset != None:
            if reset: retval += '*ZCFG'+str(zone)+'VOLRST1\r\n'
            else: retval += '*ZCFG'+str(zone)+'VOLRST0\r\n'
        return retval
    
def VOLUME( zone, level ):
    if level<0 or level>79: assert False
    return '*Z'+str(zone)+'VOL'+str(level)+'\r\n'
def VOLUMEUP( zone ):
    return '*Z'+str(zone)+'VOL+\r\n'
def VOLUMEDN( zone ):
    return '*Z'+str(zone)+'VOL-\r\n'