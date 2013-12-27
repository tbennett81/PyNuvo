from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from nuvo.models import Source, Zone

def index(request):
    return render( request, 'nuvo.html', None )
    
class SourcesView( generic.ListView ):
    template_name = 'sources/index.html'
    context_object_name = 'source_list'
    
    def get_queryset( self ):
        return Source.objects.all()
    
def sourceDetail( request, source_number ):
    source = get_object_or_404( Source, pk=source_number )
    return HttpResponse( "View Source %s" % source_number )
    
def zones( request ):
    return HttpResponse( "Zones List Page" )
    
def zoneDetail( request, zone_number ):
    return HttpResponse( "View Zone %s" % zone_number )
    
def test( request ):
    return render( request, 'sources/test.html', None )