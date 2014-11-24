from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response


# Create your views here.

def home(request):
    params = {}
    return render_to_response('supporttools/home.html',
                              params,
                              context_instance=RequestContext(request))
