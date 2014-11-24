from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
                       # for now... make the home view the default landing for
                       # /support
                       url(r'^', 'supporttools.views.home'),
                       # url(r'^', include('status_app.urls')),
                       )
