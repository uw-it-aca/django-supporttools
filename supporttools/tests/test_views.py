# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest.mock import Mock, mock_open, patch

from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
from django.test import RequestFactory, TestCase, override_settings

from supporttools.templatetags.vite import _load_manifest
from supporttools.views import SpaToolView


class TestHomeView(TestCase):
    def test_home_renders(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'supporttools/home.html')


class TestRestclientsAssets(TestCase):
    def test_restclients_script_is_a_static_asset(self):
        path = finders.find('supporttools/js/restclients.js')
        self.assertIsNotNone(path)


class TestSpaToolView(TestCase):
    def tearDown(self):
        _load_manifest.cache_clear()

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

    def test_page_data_defaults_to_empty_dict(self):
        view = self._make_view(url_name=None)
        context = view.get_context_data()
        self.assertEqual(context['page_data'], {})

    def test_page_data_is_added_to_context(self):
        class PageDataView(SpaToolView):
            def get_page_data(self):
                return {'items': [{'id': 1, 'name': 'Example'}]}

        view = PageDataView()
        request = RequestFactory().get('/')
        request.resolver_match = None
        view.request = request
        view.kwargs = {}

        context = view.get_context_data()

        self.assertEqual(context['page_data']['items'][0]['name'], 'Example')

    @patch("supporttools.templatetags.vite.open", new_callable=mock_open)
    @override_settings(VITE_MANIFEST_PATH="/static/.vite/manifest.json")
    def test_spa_template_emits_entry_styles_and_scripts(self, mocked_open):
        mocked_open.return_value.read.return_value = """{
            \"supporttools_vue/tools/my_tool.js\": {
                \"file\": \"supporttools/assets/my_tool.js\",
                \"css\": [\"supporttools/assets/my_tool.css\"]
            }
        }"""

        rendered = render_to_string(
            'supporttools/spa_tool.html',
            {
                'vite_entry': 'supporttools_vue/tools/my_tool.js',
                'page_data': {'items': [{'name': 'Example'}]},
                'supporttools_vue_enabled': True,
                'supporttools_vue_context': {},
            },
            request=RequestFactory().get('/'),
        )

        self.assertIn('supporttools/css/main.css', rendered)
        self.assertIn('supporttools/assets/my_tool.css', rendered)
        self.assertIn('supporttools/assets/my_tool.js', rendered)
        self.assertIn('supporttools-spa-page-data', rendered)
        self.assertIn('"name": "Example"', rendered)
