import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-supporttools',
    version='0.1',
    packages=['supporttools'],
    include_package_data=True,
    dependency_links = [
        'git+https://github.com/liamzebedee/scandir.git#egg=scandir-0.1',
    ],
    install_requires = [
        'setuptools',
        'django',
        'django-compressor',
        'django-templatetag-handlebars',
        'beautifulsoup',
    ],
    license='Apache License, Version 2.0',  # example license
    description='A Django app to ...',
    long_description=README,
    url='http://www.example.com/',
    author='Your Name',
    author_email='yourname@example.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
