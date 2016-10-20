[![Build Status](https://api.travis-ci.org/uw-it-aca/django-supporttools.svg?branch=master)](https://travis-ci.org/uw-it-aca/django-supporttools)
[![Coverage Status](https://coveralls.io/repos/uw-it-aca/django-supporttools/badge.png?branch=master)](https://coveralls.io/r/uw-it-aca/django-supporttools?branch=master)

ACA Support Tools
=================

A Django application used for theming and wrapping ACA support tools.

Installation
------------

**Project directory**

Install Support Tools in your project.

    $ cd [project]
    $ pip install Django-SupportTools
 
Project settings.py
------------------

**INSTALLED_APPS**

    # global support tools/apps
    'supporttools',

    # other apps that are helpful - install separately
    'restclients',
    'userservice',
    'authz_group',
    'status_app',
    
    # project specific tools/apps
    'someadminapp'

**MIDDLEWARE_CLASSES**
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_mobileesp.middleware.UserAgentDetectionMiddleware',

    # From the userservice app
    'userservice.user.UserServiceMiddleware',

**AUTHENTICATION_BACKENDS**

    'django.contrib.auth.backends.RemoteUserBackend',

**TEMPLATE_CONTEXT_PROCESSORS**
    
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    
    'supporttools.context_processors.supportools_globals',
    'supporttools.context_processors.has_less_compiled',

Mobile ESP settings...

    from django_mobileesp.detector import agent

    DETECT_USER_AGENTS = {
    'is_tablet' : agent.detectTierTablet,
    'is_mobile': agent.detectMobileQuick,
    }

Support Tools settings...

    SUPPORTTOOLS_PARENT_APP = "TestApp"
    SUPPORTTOOLS_IS_OVERRIDEABLE = True

Status App settings...

    STATUS_APP_DISPATCHERS = ['status_app.dispatcher.memory.dispatch']

    STATUS_APP_RECEIVERS = [
        'restclients.signals.rest_request.rest_request_receiver',
        'restclients.signals.success.rest_request_passfail_receiver'
    ]
    
Other settings...
    
    AUTHZ_GROUP_BACKEND = 'authz_group.authz_implementation.all_ok.AllOK'       
    USERSERVICE_ADMIN_GROUP = ' '
    RESTCLIENTS_ADMIN_GROUP = ' '
    RESTCLIENTS_SWS_DAO_CLASS = 'restclients.dao_implementation.sws.File'

Project urls.py
---------------
    # support urls - based on the support tools you install
    url(r'^someadminapp/', include('someadminapp.urls')),
    url(r'^support/', include('supporttools.urls')),
    url(r'^users/', include('userservice.urls')),
    url(r'^restclients/', include('restclients.urls')),
    url(r'^status/', include('status_app.urls')),
