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
 
Settings
-------

**INSTALLED_APPS**

    'supporttools',
    'restclients',
    'userservice',
    'authz_group',

**MIDDLEWARE_CLASSES**

    'userservice.user.UserServiceMiddleware',

**AUTHENTICATION_BACKENDS**

    'django.contrib.auth.backends.RemoteUserBackend',

**Other settings**
    
    AUTHZ_GROUP_BACKEND = 'authz_group.authz_implementation.all_ok.AllOK'       
    USERSERVICE_ADMIN_GROUP = ' '
    RESTCLIENTS_ADMIN_GROUP = ' '
    RESTCLIENTS_SWS_DAO_CLASS = 'restclients.dao_implementation.sws.File'

URLS
----

    url(r'^support/', include('supporttools.urls')),
