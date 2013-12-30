from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.views import generic

from nuvo.models import Source, Zone

def index( request ):
    cur_zone = get_object_or_404( Zone, number=1 )
    return HttpResponseRedirect(reverse('nuvo:zone_view', kwargs={'zone_name': cur_zone.name,}))
    
def model_list( request, model_name ):
    context = None
    if 'zones' == model_name:
        context = { 
            'object_list': Zone.objects.all(),
            'view_url': 'nuvo:zone_view',
            }
    elif 'sources' == model_name:
        context = { 
            'object_list': Source.objects.all(),
            'view_url': 'nuvo:source_view',
            }
    return render( request, 'model_list.html', context )
    
def zone( request, zone_name ):
    cur_zone = get_object_or_404( Zone, name=zone_name )
    enabled_sources = get_list_or_404( Source, enabled=True )
    context = { 
        'current_zone': cur_zone,
        'enabled_sources': enabled_sources,
        }
    return render( request, 'zone.html', context )
    
def source( request, source_name ):
    cur_source = get_object_or_404( Source, name=source_name )
    context = { 'current_source': cur_source }
    return render( request, 'source.html', context )