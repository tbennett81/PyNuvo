from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

def jquery( request ):
    return render( request, 'devdocs/jquery/jquery-ui.html', None )