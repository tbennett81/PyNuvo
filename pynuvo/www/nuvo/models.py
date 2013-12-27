from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(u'%s is not an even number' % value)

class Source( models.Model ):
    number = models.SmallIntegerField( primary_key=True, validators=[MinValueValidator(1), MaxValueValidator(6)] )
    name = models.CharField( max_length=20 )
    short_name = models.CharField( max_length=3 )
    active = models.BooleanField()

    #Configuration
    enabled = models.BooleanField()
    gain = models.SmallIntegerField( validators=[MinValueValidator(0), MaxValueValidator(14)] )
    nuvonet = models.BooleanField()
    use_status = models.BooleanField()
    
    #Status
    duration = models.SmallIntegerField( null=True )
    position = models.SmallIntegerField( null=True )
    
    NORMAL = 0
    IDLE = 1
    PLAYING = 2
    PAUSED = 3
    FAST_FORWARD = 4
    REWIND = 5
    PLAY_SHUFFLE = 6
    PLAY_REPEAT = 7
    PLAY_SHUFFLE_REPEAT = 8
    STATE_CHOICES = (
        ( NORMAL, 'Normal' ),
        ( IDLE, 'Idle' ),
        ( PLAYING, 'Playing' ),
        ( PAUSED, 'Paused' ),
        ( FAST_FORWARD, 'Fast Forward' ),
        ( REWIND, 'Rewind' ),
        ( PLAY_SHUFFLE, 'Play Shuffle' ),
        ( PLAY_REPEAT, 'Play Repeat' ),
        ( PLAY_SHUFFLE_REPEAT, 'Play Shuffle Repeat' ),
    )
    state = models.SmallIntegerField( choices=STATE_CHOICES )
    
    def __unicode__( self ):
        return self.name    
    
class Display( models.Model ):
    source = models.OneToOneField( Source )
    line_1 = models.CharField( max_length=30, blank=True )
    line_2 = models.CharField( max_length=30, blank=True )
    line_3 = models.CharField( max_length=30, blank=True )
    line_4 = models.CharField( max_length=30, blank=True )
    
class Zone( models.Model ):
    number = models.SmallIntegerField( primary_key=True, validators=[MinValueValidator(1), MaxValueValidator(20)] )
    name = models.CharField( max_length=20, verbose_name='description' )
    slave_to = models.ForeignKey( 'self', blank=True, null=True )
    party_host = models.BooleanField( default=False )
    active = models.BooleanField( default=True )
    #Status
    power = models.BooleanField( default=False )
    source = models.ForeignKey( Source, verbose_name='Current Source' )
    volume = models.SmallIntegerField( validators=[MinValueValidator(0), MaxValueValidator(79)], verbose_name='Current Volume' )
    mute = models.BooleanField( default=False )
    dnd = models.BooleanField( verbose_name='Do Not Disturb', default=False )
    locked = models.BooleanField( default=False )
    #Config
    enabled = models.BooleanField( default=True )
    
    GROUP_NONE = 0
    GROUP1 = 1
    GROUP2 = 2
    GROUP3 = 3
    GROUP4 = 4
    GROUP_CHOICES = (
        ( GROUP_NONE, 'None' ),
        ( GROUP1, 'Group 1' ),
        ( GROUP2, 'Group 2' ),
        ( GROUP3, 'Group 3' ),
        ( GROUP4, 'Group 4' ),
    )
        
    group = models.SmallIntegerField( choices=GROUP_CHOICES, default=GROUP_NONE )
    exclusive = models.BooleanField( verbose_name='Exclusive Source Control', default=False )
    
    IR_ENABLED = 0
    PASS_THRU_DISABLED = 1
    ALL_DISABLED = 2
    IR_CHOICES = (
        ( IR_ENABLED, 'IR Enabled' ),
        ( PASS_THRU_DISABLED, 'IR pass-thru disabled' ),
        ( ALL_DISABLED, 'All Disabled' ),
    )
    ir = models.SmallIntegerField( choices=IR_CHOICES, verbose_name='IR Control', default=IR_ENABLED )
    default_lock = models.BooleanField( verbose_name='Lock zone by default', default=False )

    #Do not Disturb Behavior
    no_mute = models.BooleanField( default=False )
    no_page = models.BooleanField( default=False )
    no_party = models.BooleanField( default=False )

    #Valid Sources
    source_1 = models.BooleanField( default=True )
    source_2 = models.BooleanField( default=True )
    source_3 = models.BooleanField( default=True )
    source_4 = models.BooleanField( default=True )
    source_5 = models.BooleanField( default=True )
    source_6 = models.BooleanField( default=True )

    #Equalizer
    bass = models.SmallIntegerField( validators=[MinValueValidator(-18), MaxValueValidator(18), validate_even], default=0 )
    treble = models.SmallIntegerField( validators=[MinValueValidator(-18), MaxValueValidator(18), validate_even], default=0 )
    balance = models.SmallIntegerField( validators=[MinValueValidator(-18), MaxValueValidator(18), validate_even], default=0 )
    loudness = models.BooleanField( verbose_name='Loudness Compensation', default=False )

    #Volume
    max_volume = models.SmallIntegerField( validators=[MinValueValidator(0), MaxValueValidator(79)], default=79 )
    initial_volume = models.SmallIntegerField( validators=[MinValueValidator(0), MaxValueValidator(79)], default=25 )
    page_volume = models.SmallIntegerField( validators=[MinValueValidator(0), MaxValueValidator(79)], default=25 )
    party_volume = models.SmallIntegerField( validators=[MinValueValidator(0), MaxValueValidator(79)], default=25 )
    volume_reset = models.BooleanField( verbose_name='Reset Volume at Zone Power', default=False )

    #Control Pad
    brightness = models.SmallIntegerField( validators=[MinValueValidator(1), MaxValueValidator(7)], default=7 )
    auto_dim = models.SmallIntegerField( validators=[MinValueValidator(0), MaxValueValidator(8)], default=0 )
    dim = models.SmallIntegerField( validators=[MinValueValidator(0), MaxValueValidator(3)], default=3 )
    time = models.BooleanField( verbose_name='Display Time when Off', default=True )
    
    def __unicode__(self):
        return self.name