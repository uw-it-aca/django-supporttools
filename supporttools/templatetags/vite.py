# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import functools
import json
import logging
import os

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

logger = logging.getLogger(__name__)


def _manifest_filepaths():
    configured = getattr(settings, "VITE_MANIFEST_PATH", None)
    defaults = [
        os.path.join(os.sep, "static", "manifest.json"),
        os.path.join(os.sep, "static", ".vite", "manifest.json"),
    ]

    if configured:
        return [configured] + defaults
    return defaults


@functools.lru_cache(maxsize=None)
def _load_manifest():
    for path in _manifest_filepaths():
        try:
            with open(path) as fp:
                return json.load(fp)
        except FileNotFoundError:
            continue
    raise FileNotFoundError("Vite manifest file was not found")


def vite_manifest(entry_names):
    manifest = _load_manifest()
    processed = set()

    def process_entries(names):
        scripts = []
        styles = []

        for name in names:
            if name in processed:
                continue

            chunk = manifest.get(name)
            if chunk is None:
                continue
            import_scripts, import_styles = process_entries(
                chunk.get("imports", [])
            )
            scripts += import_scripts
            styles += import_styles

            scripts += [chunk["file"]]
            styles += [css for css in chunk.get("css", [])]
            processed.add(name)

        return scripts, styles

    return process_entries(entry_names)


@register.simple_tag(name="vite_styles")
def vite_styles(*entry_names):
    try:
        _, styles = vite_manifest(entry_names)
    except FileNotFoundError:
        logger.warning("vite_styles: manifest not found; no styles emitted")
        return mark_safe("")

    def as_link_tag(href):
        return format_html('<link rel="stylesheet" href="{}" />', static(href))

    return mark_safe("\n".join(map(as_link_tag, styles)))


@register.simple_tag(name="vite_scripts")
def vite_scripts(*entry_names):
    try:
        scripts, _ = vite_manifest(entry_names)
    except FileNotFoundError:
        logger.warning("vite_scripts: manifest not found; no scripts emitted")
        return mark_safe("")

    def as_script_tag(src):
        return format_html('<script type="module" src="{}"></script>', static(src))

    return mark_safe("\n".join(map(as_script_tag, scripts)))
