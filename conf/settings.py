STATIC_ROOT = ''

INSTALLED_APPS += [
    'supporttools',
    'django_user_agents',
]

MIDDLEWARE += [
    'django_user_agents.middleware.UserAgentMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.RemoteUserBackend',
]
