STATIC_ROOT = ''

INSTALLED_APPS += [
    'supporttools',
    'compressor',
    'django_user_agents',
]

MIDDLEWARE += [
    'django_user_agents.middleware.UserAgentMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.RemoteUserBackend',
]
