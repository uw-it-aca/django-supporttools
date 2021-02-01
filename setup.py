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
    author="UW-IT AXDD",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'django>2.1,<3.2',
        'django-userservice>3.1,<4.0',
        'django-user-agents',
    ],
    license='Apache License, Version 2.0',
    description=('A Django application used for theming and wrapping '
                 'AXDD support tools.'),
    long_description=README,
    url=url,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
