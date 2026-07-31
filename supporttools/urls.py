# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import re

from django.conf import settings
from django.urls import re_path
from django.utils.module_loading import import_string

from supporttools.views import HomeView, SpaToolView

urlpatterns = [
    re_path(r'^', HomeView.as_view(), name='supporttools_home'),
]


def get_registry_urlpatterns():
    """Return URL patterns auto-generated from SUPPORTTOOLS_VIEW_REGISTRY.

    For each SPA entry that declares url_name and route, a re_path() is
    created using whichever view class is resolved in this order:
      1. Entry's own "view" key (dotted import path)
      2. SUPPORTTOOLS_DEFAULT_SPA_VIEW setting (dotted import path)
      3. SpaToolView fallback
    """
    registry = getattr(settings, 'SUPPORTTOOLS_VIEW_REGISTRY', [])
    default_view_path = getattr(
        settings, 'SUPPORTTOOLS_DEFAULT_SPA_VIEW', None
    )

    patterns = []
    for entry in registry:
        if entry.get('mode') != 'spa':
            continue
        url_name = entry.get('url_name')
        route = entry.get('route')
        if not url_name or not route:
            continue

        view_path = entry.get('view') or default_view_path
        if view_path:
            view_class = import_string(view_path)
        else:
            view_class = SpaToolView

        # Escape the literal route string for use as a regex pattern,
        # then anchor it so it matches only that exact path.
        pattern = r'^' + re.escape(route.lstrip('/')) + r'$'
        patterns.append(
            re_path(pattern, view_class.as_view(), name=url_name)
        )

    return patterns
