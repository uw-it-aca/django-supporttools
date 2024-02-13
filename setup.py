import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/django-supporttools>`_.
"""

version_path = 'supporttools/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = "https://github.com/uw-it-aca/django-supporttools"
setup(
    name='Django-SupportTools',
    version=VERSION,
    packages=['supporttools'],
    author="UW-IT T&LS",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'Django>3.2,<5',
        'django-userservice',
        'django-user-agents',
        'mock',
    ],
    license='Apache License, Version 2.0',
    description=('A Django application used for theming and wrapping '
                 'T&LS support tools.'),
    long_description=README,
    url=url,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
