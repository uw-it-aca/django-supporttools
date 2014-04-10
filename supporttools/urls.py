from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    
    url(r'^status', include('status_app.urls')),
    url(r'^users', include('userservice.urls')),
    url(r'^restclients', include('restclients.urls')),
    url(r'^', 'supporttools.views.home'),
    #url(r'^', include('status_app.urls')),
    
)
