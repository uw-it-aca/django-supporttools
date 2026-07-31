# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest.mock import Mock

from django.test import RequestFactory, TestCase, override_settings

from supporttools.views import SpaToolView


class TestHomeView(TestCase):
    def test_home_renders(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'supporttools/home.html')


class TestSpaToolView(TestCase):
    def _make_view(self, url_name=None):
        view = SpaToolView()
        request = RequestFactory().get('/')
        if url_name is not None:
            request.resolver_match = Mock()
            request.resolver_match.url_name = url_name
        else:
            request.resolver_match = None
        view.request = request
        view.kwargs = {}
        return view

    @override_settings(SUPPORTTOOLS_VIEW_REGISTRY=[{
        'label': 'My Tool',
        'url_name': 'my_tool',
        'mode': 'spa',
        'route': '/support/my-tool',
        'component_key': 'my_tool_component',
        'vite_entry': 'supporttools_vue/tools/my_tool.js',
    }])
    def test_vite_entry_from_matching_registry_entry(self):
        view = self._make_view(url_name='my_tool')
        context = view.get_context_data()
        self.assertEqual(context['vite_entry'],
                         'supporttools_vue/tools/my_tool.js')

    @override_settings(SUPPORTTOOLS_VIEW_REGISTRY=[])
    def test_vite_entry_empty_when_no_match(self):
        view = self._make_view(url_name='nonexistent')
        context = view.get_context_data()
        self.assertEqual(context['vite_entry'], '')

    def test_vite_entry_empty_when_no_resolver_match(self):
        view = self._make_view(url_name=None)
        context = view.get_context_data()
        self.assertEqual(context['vite_entry'], '')
