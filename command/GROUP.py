from consts import *

def MSG( group, msg, msg_type = INFORMATION, msg_time = NORMAL ):
	if group<0 or group>3: assert False
	if msg_type<0 or msg_type>3: assert False
	if msg_time<0 or msg_time>2: assert False
	return '*G'+str(group)+'MSG"'+msg[0:20]+'",'+str(msg_type)+','+str(msg_time)+'\r\n'
def OFF( group ):
	if group<0 or group>3: assert False
	return '*G'+str(group)+'OFF\r\n'
