from django.shortcuts import render_to_response
from django.template import RequestContext

def plantshare_view(request):
    return render_to_response('plantshare.html', {
           }, context_instance=RequestContext(request))

def join_view(request):
    return render_to_response('join.html', {
           }, context_instance=RequestContext(request))