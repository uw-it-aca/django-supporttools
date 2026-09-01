STATIC_ROOT = ''

VITE_MANIFEST_PATH = '/static/manifest.json'
SUPPORTTOOLS_VUE_ENABLED = False

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
