# AXDD Support Tools

[![Build Status](https://github.com/uw-it-aca/django-supporttools/workflows/tests/badge.svg?branch=main)](https://github.com/uw-it-aca/django-supporttools/actions)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/django-supporttools/badge.svg?branch=main)](https://coveralls.io/github/uw-it-aca/django-supporttools?branch=main)
[![PyPi Version](https://img.shields.io/pypi/v/django-supporttools.svg)](https://pypi.python.org/pypi/django-supporttools)
![Python versions](https://img.shields.io/pypi/pyversions/django-supporttools.svg)


A Django application used for theming and wrapping support tools.

### Installation

This should be installed as a dependency in your project.  You should not install this manually.

### Configuration

Add these values to your project's settings.py:

```
MIDDLEWARE = [
    ...
    'userservice.user.UserServiceMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

INSTALLED_APPS = [
    ...
    'supporttools',
    'userservice',
    'compressor',
    'django_user_agents',
]

TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                ...
                'django.template.context_processors.request',
                'supporttools.context_processors.supportools_globals',
                'supporttools.context_processors.has_less_compiled',
            ],
        },
    },  
]

# Where the back link should go, and how it's labeled.
SUPPORTTOOLS_PARENT_APP = "TestApp"
SUPPORTTOOLS_PARENT_APP_URL = "/"
```
