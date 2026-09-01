# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import re

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import re_path
from django.utils.module_loading import import_string

from supporttools.context_processors import normalize_mode_fields
from supporttools.views import HomeView


def get_registry_urlpatterns():
    """Return URL patterns auto-generated from SUPPORTTOOLS_VIEW_REGISTRY.

    For each SPA entry that declares url_name and route, a re_path() is
    created using whichever view class is resolved in this order:
      1. Entry's own "view" key (dotted import path)
      2. SUPPORTTOOLS_DEFAULT_SPA_VIEW setting (dotted import path)

    Each generated SPA route must use an explicitly configured view so that
    consuming applications cannot accidentally omit their auth policy.
    """
    registry = getattr(settings, 'SUPPORTTOOLS_VIEW_REGISTRY', [])
    default_view_path = getattr(
        settings, 'SUPPORTTOOLS_DEFAULT_SPA_VIEW', None
    )

    patterns = []
    for entry in registry:
        mode_fields = normalize_mode_fields(entry)
        if not mode_fields or mode_fields['mode'] != 'spa':
            continue
        url_name = entry.get('url_name')
        route = entry.get('route')
        if not url_name or not route:
            continue

        view_path = entry.get('view') or default_view_path
        if not view_path:
            raise ImproperlyConfigured(
                "SPA supporttools registry entry {!r} must define 'view' or "
                "SUPPORTTOOLS_DEFAULT_SPA_VIEW must be configured.".format(
                    entry.get('id') or url_name
                )
            )
        view_class = import_string(view_path)

        # Escape the literal route string for use as a regex pattern,
        # then anchor it so it matches only that exact path.
        pattern = r'^' + re.escape(route.lstrip('/')) + r'$'
        patterns.append(
            re_path(pattern, view_class.as_view(), name=url_name)
        )

    return patterns


# SPA routes must precede the legacy catch-all home route so direct navigation
# resolves to the configured SPA view.
urlpatterns = get_registry_urlpatterns() + [
    re_path(r'^', HomeView.as_view(), name='supporttools_home'),
]
