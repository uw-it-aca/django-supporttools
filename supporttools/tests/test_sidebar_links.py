import os

from django.test import TestCase
from django.template import Context, Template


class TestSidebarLinks(TestCase):
    def test_default_sidebar(self):
        with self.settings(TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': '',
            'APP_DIRS': True,
        }]):
            out = Template('{% load sidebar_links %}'
                           '{% sidebar_links %}').render(Context())

            self.assertInHTML('<h3>General Tools</h3>', out)

    def test_custom_sidebar(self):
        with self.settings(TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(os.path.dirname(__file__), 'test_templates')],
            'APP_DIRS': True,
        }]):
            out = Template('{% load sidebar_links %}'
                           '{% sidebar_links %}').render(Context())

            self.assertInHTML('<h3>Custom Tools</h3>', out)
