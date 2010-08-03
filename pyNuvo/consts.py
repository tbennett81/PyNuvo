import ctypes

class StatusType(ctypes.c_ulong):
	_names= {
		0: 'Normal',
		1: 'Idle',
		2: 'Playing',
		3: 'Paused',
		4: 'FastForward',
		5: 'Rewind',
		6: 'PlayShuffle',
		7: 'PlayRepeat',
		8: 'PlayShuffleRepeat',
	}
	
	def __repr__(self):
		return ".".join((self.__class__.__module__, self.__class__.__name__, self._names[self.value]))
		
	def __eq__(self, other):
		return( ( isinstance(other, ctypes.c_ulong) and self.value == other.value )
				or (isinstance(other, (int,long)) and self.value == other ) )
				
	def __ne__(self, other):
		return not self.__eq__(other)
		
StatusType.Normal=StatusType(0)
StatusType.Idle=StatusType(1)
StatusType.Playing=StatusType(2)
StatusType.Paused=StatusType(3)
StatusType.FastForward=StatusType(4)
StatusType.Rewind=StatusType(5)
StatusType.PlayShuffle=StatusType(6)
StatusType.PlayRepeat=StatusType(7)
StatusType.PlayShuffleRepeat=StatusType(8)

class MsgTimeType(ctypes.c_ulong):
	_names= {
		0: 'Normal',
		1: 'Short',
		2: 'Long',
	}
	
	def __repr__(self):
		return ".".join((self.__class__.__module__, self.__class__.__name__, self._names[self.value]))
		
	def __eq__(self, other):
		return( ( isinstance(other, ctypes.c_ulong) and self.value == other.value )
				or (isinstance(other, (int,long)) and self.value == other ) )
				
	def __ne__(self, other):
		return not self.__eq__(other)
		
MsgTimeType.Normal=MsgTimeType(0)
MsgTimeType.Short=MsgTimeType(1)
MsgTimeType.Long=MsgTimeType(2)

class StateType(ctypes.c_ulong):
	_names= {
		0: 'Disable',
		1: 'Enable',
	}
	
	def __repr__(self):
		return ".".join((self.__class__.__module__, self.__class__.__name__, self._names[self.value]))
		
	def __eq__(self, other):
		return( ( isinstance(other, ctypes.c_ulong) and self.value == other.value )
				or (isinstance(other, (int,long)) and self.value == other ) )
				
	def __ne__(self, other):
		return not self.__eq__(other)
		
StateType.Disable=StateType(0)
StateType.Enable=StateType(1)

class NuvoNetType(ctypes.c_ulong):
	_names= {
		0: 'IRSource',
		1: 'NuvoNet',
	}
	
	def __repr__(self):
		return ".".join((self.__class__.__module__, self.__class__.__name__, self._names[self.value]))
		
	def __eq__(self, other):
		return( ( isinstance(other, ctypes.c_ulong) and self.value == other.value )
				or (isinstance(other, (int,long)) and self.value == other ) )
				
	def __ne__(self, other):
		return not self.__eq__(other)
		
NuvoNetType.IRSource=NuvoNetType(0)
NuvoNetType.NuvoNet=NuvoNetType(1)

class TimeFormatType(ctypes.c_ulong):
	_names= {
		0: 'Time12Hour',
		1: 'Time24Hour',
	}
	
	def __repr__(self):
		return ".".join((self.__class__.__module__, self.__class__.__name__, self._names[self.value]))
		
	def __eq__(self, other):
		return( ( isinstance(other, ctypes.c_ulong) and self.value == other.value )
				or (isinstance(other, (int,long)) and self.value == other ) )
				
	def __ne__(self, other):
		return not self.__eq__(other)
		
TimeFormatType.Time12Hour=TimeFormatType(0)
TimeFormatType.Time24Hour=TimeFormatType(1)

class IRStateType(ctypes.c_ulong):
	_names= {
		0: 'IREnable',
		1: 'IRNoPassThru',
		2: 'IRDisable',
	}
	
	def __repr__(self):
		return ".".join((self.__class__.__module__, self.__class__.__name__, self._names[self.value]))
		
	def __eq__(self, other):
		return( ( isinstance(other, ctypes.c_ulong) and self.value == other.value )
				or (isinstance(other, (int,long)) and self.value == other ) )
				
	def __ne__(self, other):
		return not self.__eq__(other)
		
IRStateType.IREnable=IRStateType(0)
IRStateType.IRNoPassThru=IRStateType(1)
IRStateType.IRDisable=IRStateType(2)

class MessageType(ctypes.c_ulong):
	_names= {
		0: 'Information',
		1: 'Warning',
		2: 'Error',
		3: 'Flash',
	}
	
	def __repr__(self):
		return ".".join((self.__class__.__module__, self.__class__.__name__, self._names[self.value]))
		
	def __eq__(self, other):
		return( ( isinstance(other, ctypes.c_ulong) and self.value == other.value )
				or (isinstance(other, (int,long)) and self.value == other ) )
				
	def __ne__(self, other):
		return not self.__eq__(other)
		
MessageType.Information=MessageType(0)
MessageType.Warning=MessageType(1)
MessageType.Error=MessageType(2)
MessageType.Flash=MessageType(3)
