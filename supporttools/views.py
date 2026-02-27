# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'supporttools/home.html'
