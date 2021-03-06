from django.contrib import admin
from nuvo.models import Source, Zone
        
class SourceAdmin( admin.ModelAdmin ):
    fieldsets = [
        ( None, { 'fields': ['number', 'name', 'short_name', 'active'] } ),
        ( 'Configuration', { 'fields': ['enabled', 'gain', 'nuvonet', 'use_status'] } ),
        ( 'Display', { 'fields': [ 'display_line_1', 'display_line_2', 'display_line_3', 'display_line_4' ] } ),
        ( 'Status', { 'fields': [ 'duration', 'position', 'state' ] } ),
        ]
    
class ZoneAdmin(admin.ModelAdmin):
    fieldsets = [
        ( None, { 'fields': ['number', 'name', 'party_host', 'active'] } ),
        ( 'Status', { 'fields': ['power', 'source', 'volume', 'dnd', 'locked'] } ),
        ( 'Configuration', { 'fields': ['enabled', 'group', 'exclusive', 'ir'] } ),
        ( 'Do not Disturb Behavior', { 'fields': ['no_mute', 'no_page', 'no_party'] } ),
        ( 'Equalizer', { 'fields': ['bass', 'treble', 'balance', 'loudness'] } ),
        ( 'Volume', { 'fields': [ 'max_volume', 'initial_volume', 'page_volume', 'party_volume', 'volume_reset'] } ),
        ( 'Sources Allowed', { 'fields': ['source_1', 'source_2', 'source_3', 'source_4', 'source_5', 'source_6'] } ),
        ( 'Control Pad', { 'fields': ['brightness', 'auto_dim', 'dim', 'time'] } ),
    ]

admin.site.register( Source, SourceAdmin )
admin.site.register( Zone, ZoneAdmin )