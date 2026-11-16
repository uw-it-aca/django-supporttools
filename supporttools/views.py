# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.conf import settings
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'supporttools/home.html'


class SpaToolView(TemplateView):
    """Base view for SPA support tools.

    Auth is the responsibility of the consuming app (e.g. via method_decorator
    on dispatch in a project-specific subclass).
    """

    template_name = 'supporttools/spa_tool.html'

    def get_page_data(self):
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registry = getattr(settings, 'SUPPORTTOOLS_VIEW_REGISTRY', [])
        url_name = (
            self.request.resolver_match.url_name
            if self.request.resolver_match else None
        )
        entry = next(
            (e for e in registry if e.get('url_name') == url_name), {}
        )
        context['vite_entry'] = entry.get('vite_entry', '')
        context['page_data'] = self.get_page_data()
        return context
