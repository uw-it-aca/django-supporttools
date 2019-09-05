from django.shortcuts import render
from django.conf import settings


def home(request):
    return render(request, 'supporttools/home.html', {
        'has_compress': ('compress' in settings.INSTALLED_APPS)
    })
