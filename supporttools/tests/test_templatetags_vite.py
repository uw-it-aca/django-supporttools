# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest.mock import mock_open, patch

from django.test import TestCase, override_settings

from supporttools.templatetags.vite import (
    _load_manifest,
    _manifest_filepaths,
    vite_scripts,
    vite_styles,
)


class TestViteTemplateTags(TestCase):
    def tearDown(self):
        _load_manifest.cache_clear()

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


class TestManifestFilepaths(TestCase):
    def test_configured_path_is_first(self):
        with self.settings(VITE_MANIFEST_PATH="/custom/manifest.json"):
            paths = _manifest_filepaths()
        self.assertEqual(paths[0], "/custom/manifest.json")

    def test_defaults_returned_when_not_configured(self):
        with self.settings(VITE_MANIFEST_PATH=None):
            paths = _manifest_filepaths()
        self.assertTrue(len(paths) > 0)
        self.assertNotIn(None, paths)


class TestLoadManifest(TestCase):
    def tearDown(self):
        _load_manifest.cache_clear()

    @patch("supporttools.templatetags.vite.open", side_effect=FileNotFoundError)
    def test_raises_when_all_paths_fail(self, _):
        with self.assertRaises(FileNotFoundError):
            _load_manifest()

    @patch("supporttools.templatetags.vite.open", new_callable=mock_open)
    @override_settings(VITE_MANIFEST_PATH="/priority/manifest.json")
    def test_configured_path_opened_first(self, mocked_open):
        mocked_open.return_value.read.return_value = '{"entry": {"file": "x.js"}}'
        _load_manifest()
        first_call_path = mocked_open.call_args_list[0][0][0]
        self.assertEqual(first_call_path, "/priority/manifest.json")


class TestViteManifestChainedImports(TestCase):
    def tearDown(self):
        _load_manifest.cache_clear()

    CHAINED_MANIFEST = """{
        "supporttools_vue/main.js": {
            "file": "supporttools/assets/main.js",
            "imports": ["supporttools_vue/chunk.js"],
            "css": ["supporttools/assets/main.css"]
        },
        "supporttools_vue/chunk.js": {
            "file": "supporttools/assets/chunk.js",
            "css": ["supporttools/assets/chunk.css"]
        }
    }"""

    @patch("supporttools.templatetags.vite.open", new_callable=mock_open)
    @override_settings(VITE_MANIFEST_PATH="/static/.vite/manifest.json")
    def test_chained_import_styles_included(self, mocked_open):
        mocked_open.return_value.read.return_value = self.CHAINED_MANIFEST
        style_tag = vite_styles("supporttools_vue/main.js")
        self.assertIn("supporttools/assets/chunk.css", style_tag)
        self.assertIn("supporttools/assets/main.css", style_tag)

    @patch("supporttools.templatetags.vite.open", new_callable=mock_open)
    @override_settings(VITE_MANIFEST_PATH="/static/.vite/manifest.json")
    def test_chained_import_scripts_included(self, mocked_open):
        mocked_open.return_value.read.return_value = self.CHAINED_MANIFEST
        script_tag = vite_scripts("supporttools_vue/main.js")
        self.assertIn("supporttools/assets/chunk.js", script_tag)
        self.assertIn("supporttools/assets/main.js", script_tag)

    @patch("supporttools.templatetags.vite.open", new_callable=mock_open)
    @override_settings(VITE_MANIFEST_PATH="/static/.vite/manifest.json")
    def test_duplicate_imports_not_repeated(self, mocked_open):
        # Two entries both import the same chunk — chunk should appear once.
        mocked_open.return_value.read.return_value = """{
            "supporttools_vue/a.js": {
                "file": "supporttools/assets/a.js",
                "imports": ["supporttools_vue/chunk.js"],
                "css": []
            },
            "supporttools_vue/b.js": {
                "file": "supporttools/assets/b.js",
                "imports": ["supporttools_vue/chunk.js"],
                "css": []
            },
            "supporttools_vue/chunk.js": {
                "file": "supporttools/assets/chunk.js",
                "css": []
            }
        }"""
        script_tag = vite_scripts(
            "supporttools_vue/a.js", "supporttools_vue/b.js"
        )
        self.assertEqual(script_tag.count("chunk.js"), 1)


class TestViteTagsEscaping(TestCase):
    def tearDown(self):
        _load_manifest.cache_clear()

    @patch("supporttools.templatetags.vite.open", new_callable=mock_open)
    @override_settings(VITE_MANIFEST_PATH="/static/.vite/manifest.json")
    def test_styles_manifest_path_with_quotes_is_escaped(self, mocked_open):
        mocked_open.return_value.read.return_value = """{
            "supporttools_vue/main.js": {
                "file": "supporttools/assets/main.js",
                "css": ["supporttools/assets/\\"injected.css"]
            }
        }"""
        style_tag = vite_styles("supporttools_vue/main.js")
        self.assertNotIn('href=""', style_tag)

    @patch("supporttools.templatetags.vite.open", new_callable=mock_open)
    @override_settings(VITE_MANIFEST_PATH="/static/.vite/manifest.json")
    def test_scripts_manifest_path_with_quotes_is_escaped(self, mocked_open):
        mocked_open.return_value.read.return_value = """{
            "supporttools_vue/main.js": {
                "file": "supporttools/assets/\\"injected.js",
                "css": []
            }
        }"""
        script_tag = vite_scripts("supporttools_vue/main.js")
        self.assertNotIn('src=""', script_tag)

