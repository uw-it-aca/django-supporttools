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

    'supporttools',
    'restclients',
    'userservice',
    'authz_group',

**MIDDLEWARE_CLASSES**

    'userservice.user.UserServiceMiddleware',
    'django_mobileesp.middleware.UserAgentDetectionMiddleware',

**AUTHENTICATION_BACKENDS**

    'django.contrib.auth.backends.RemoteUserBackend',

**TEMPLATE_CONTEXT_PROCESSORS**

    'supporttools.context_processors.global_supportools_stuff',

Support Tools settings...

    SUPPORTTOOLS_PARENT_APP = "TestApp"
    
Other settings...
    
    AUTHZ_GROUP_BACKEND = 'authz_group.authz_implementation.all_ok.AllOK'       
    USERSERVICE_ADMIN_GROUP = ' '
    RESTCLIENTS_ADMIN_GROUP = ' '
    RESTCLIENTS_SWS_DAO_CLASS = 'restclients.dao_implementation.sws.File'

Project urls.py
---------------

    url(r'^support/', include('supporttools.urls')),
