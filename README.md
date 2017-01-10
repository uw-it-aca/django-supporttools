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

    'django_mobileesp.middleware.UserAgentDetectionMiddleware',
    'userservice.user.UserServiceMiddleware',

Note: django_mobileesp does not support the new-style middleware, so you must use MIDDLEWARE_CLASSES instead of MIDDLEWARE if you are on Django 1.10 or higher.

**INSTALLED_APPS**

    'supporttools',
    'django_mobileesp',


**TEMPLATE_CONTEXT_PROCESSORS**

Pre Django 1.10, add these values to your TEMPLATE_CONTEXT_PROCESSORS setting.

For Django 1.10, add them to TEMPLATES.OTPIONS.context_processors.

    'supporttools.context_processors.supportools_globals',
    'supporttools.context_processors.has_less_compiled',

Mobile ESP settings...

    from django_mobileesp.detector import mobileesp_agent as agent

    DETECT_USER_AGENTS = {
    'is_tablet' : agent.detectTierTablet,
    'is_mobile': agent.detectMobileQuick,
    }

Support Tools settings...

    # Where the back link should go, and how it's labelled.
    SUPPORTTOOLS_PARENT_APP = "TestApp"
    SUPPORTTOOLS_PARENT_APP_URL = "/"
