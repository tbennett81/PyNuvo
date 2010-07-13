###############################Source Constants################################
#Enable / Disable Feature
DISABLE, ENABLE = range(0,2)
#Nuvonet Device
IR_SOURCE, NUVONET = range(0,2)
#Play Mode
NORMAL, IDLE, PLAYING, PAUSED, FAST_FORWARD, REWIND, PLAY_SHUFFLE, PLAY_REPEAT, PLAY_SHUFFLE_REPEAT = range(0,9)

###############################System Constants################################
#Time Formats
TIME_12HOUR, TIME_24HOUR = range(0,2)

################################Zone Constants#################################
#IR State Variables
IR_ENABLE, IR_NO_PASSTHRU, IR_DISABLE = range(0,3)

##############################Message Constants################################
#Message Type
INFORMATION, WARNING, ERROR, FLASH = range(0, 4)
#Message Length
SHORT, LONG = range(1, 3) #NORMAL = 0 already defined in Source Play Mode
