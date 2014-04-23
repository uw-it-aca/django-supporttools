ACA Support Tools
=================

A Django application used for theming and wrapping ACA support tools.

Installation
------------

**Project directory**

Install Support Tools in your project.

    $ cd [project]
    $ pip install -e git+https://github.com/charlon/django-supporttools/#egg=django_supporttools

**Install dependencies**

Pip install the requirements.txt that was included.

    $ cd [virtualenv] /src
    $ pip install -r django-supporttools/requirements.txt
 
Project settings.py
------------------

**INSTALLED_APPS**

    # global support tools/apps
    'supporttools',
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

**TEMPLATE_DIRS**

    'os.path.join(BASE_DIR, 'supporttools', 'templates'),'

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
    # support urls
    url(r'^support/someadminapp/', include('someadminapp.urls')),
    url(r'^support/', include('supporttools.urls')),
