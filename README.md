[![Build Status](https://api.travis-ci.org/uw-it-aca/django-supporttools.svg?branch=master)](https://travis-ci.org/uw-it-aca/django-supporttools)
[![Coverage Status](https://coveralls.io/repos/uw-it-aca/django-supporttools/badge.png?branch=master)](https://coveralls.io/r/uw-it-aca/django-supporttools?branch=master)

ACA Support Tools
=================

A Django application used for theming and wrapping support tools.

Installation
------------

This should be installed as a requirement from a support tool.  You should not install this manually.


Project settings.py
------------------

Add these values to your project's settings.py:

**MIDDLEWARE_CLASSES**

    'userservice.user.UserServiceMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',


**INSTALLED_APPS**

    'supporttools',
    'compressor',
    'django_user_agents',


**TEMPLATE_CONTEXT_PROCESSORS**

Add to TEMPLATES.OPTIONS.context_processors.

    'django.template.context_processors.request',
    'supporttools.context_processors.supportools_globals',
    'supporttools.context_processors.has_less_compiled',


Support Tools settings...

    # Where the back link should go, and how it's labelled.
    SUPPORTTOOLS_PARENT_APP = "TestApp"
    SUPPORTTOOLS_PARENT_APP_URL = "/"
