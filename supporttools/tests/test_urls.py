# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from importlib import reload

from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase, override_settings
from django.urls.resolvers import RegexPattern, URLResolver

import supporttools.urls
from supporttools.views import SpaToolView


class TestRegistryUrls(SimpleTestCase):
    @override_settings(SUPPORTTOOLS_VIEW_REGISTRY=[{
        'label': 'My Tool',
        'url_name': 'my_tool',
        'mode': 'spa',
        'route': '/support/my-tool/',
        'component_key': 'my_tool_component',
        'view': 'supporttools.views.SpaToolView',
    }])
    def test_spa_route_precedes_home_fallback(self):
        urlconf = reload(supporttools.urls)
        self.addCleanup(reload, urlconf)
        resolver = URLResolver(RegexPattern(r'^'), urlconf.urlpatterns)

        match = resolver.resolve('support/my-tool/')

        self.assertIs(match.func.view_class, SpaToolView)

    @override_settings(
        SUPPORTTOOLS_DEFAULT_SPA_VIEW='supporttools.views.SpaToolView',
        SUPPORTTOOLS_VIEW_REGISTRY=[{
            'label': 'Converted Tool',
            'url_name': 'converted_tool',
            'route': '/support/converted-tool/',
            'component_key': 'converted_tool_component',
            'vite_entry': 'myapp_vue/support/converted-tool.js',
        }],
    )
    def test_spa_marker_fields_register_route_without_mode(self):
        urlconf = reload(supporttools.urls)
        self.addCleanup(reload, urlconf)
        resolver = URLResolver(RegexPattern(r'^'), urlconf.urlpatterns)

        match = resolver.resolve('support/converted-tool/')

        self.assertIs(match.func.view_class, SpaToolView)

    @override_settings(SUPPORTTOOLS_VIEW_REGISTRY=[{
        'id': 'unprotected_tool',
        'label': 'Unprotected Tool',
        'url_name': 'unprotected_tool',
        'mode': 'spa',
        'route': '/support/unprotected-tool/',
        'component_key': 'unprotected_tool_component',
    }])
    def test_spa_route_requires_explicit_or_default_view(self):
        with self.assertRaisesMessage(
                ImproperlyConfigured,
                "SPA supporttools registry entry 'unprotected_tool' must "
                "define 'view' or SUPPORTTOOLS_DEFAULT_SPA_VIEW must be "
                "configured."):
            reload(supporttools.urls)