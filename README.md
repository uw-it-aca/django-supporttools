ACA Support Tools
=================

A Django app for creating a support tool for individual apps.

Install for development
=======================

* create virtualenv
* pip install django
* pip install django-compressor
* pip install django-templatetag-handlebars
* create django project
* cd project
* pip install -e git+https://github.com/charlon/django-supporttools/#egg=django_supporttools
* pip install -e svn+https://svn.cac.washington.edu/svn/restclients/trunk#egg=RestClients
* pip install -e git+https://github.com/vegitron/django-userservice#egg=Django-UserService
* pip install -e git+https://github.com/vegitron/authz_group#egg=AuthZ-Group
* pip install -e git+https://github.com/abztrakt/django-mobileesp/#egg=django_mobileesp


* update project settings.py
* add support reference to urls.py

Installation on apps
====================
* pip install the app via github or pypi
