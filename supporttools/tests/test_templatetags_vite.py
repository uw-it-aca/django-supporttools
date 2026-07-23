# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest.mock import mock_open, patch
from django.test import TestCase, override_settings
from supporttools.templatetags.vite import vite_scripts, vite_styles


class TestViteTemplateTags(TestCase):
    @patch("supporttools.templatetags.vite.open", new_callable=mock_open)
    @override_settings(VITE_MANIFEST_PATH="/static/.vite/manifest.json")
    def test_vite_styles(self, mocked_open):
        mocked_open.return_value.read.return_value = """{
            \"supporttools_vue/main.js\": {
                \"file\": \"supporttools/assets/main.js\",
                \"css\": [\"supporttools/assets/main.css\"]
            }
        }"""

        style_tag = vite_styles("supporttools_vue/main.js")
        self.assertIn("supporttools/assets/main.css", style_tag)
        mocked_open.assert_called_with("/static/.vite/manifest.json")

    @patch("supporttools.templatetags.vite.open", new_callable=mock_open)
    @override_settings(VITE_MANIFEST_PATH="/static/.vite/manifest.json")
    def test_vite_scripts(self, mocked_open):
        mocked_open.return_value.read.return_value = """{
            \"supporttools_vue/main.js\": {
                \"file\": \"supporttools/assets/main.js\",
                \"css\": [\"supporttools/assets/main.css\"]
            }
        }"""

        script_tag = vite_scripts("supporttools_vue/main.js")
        self.assertIn("supporttools/assets/main.js", script_tag)
        mocked_open.assert_called_with("/static/.vite/manifest.json")
