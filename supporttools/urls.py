# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.urls import re_path
from supporttools.views import HomeView

urlpatterns = [
    re_path(r'^', HomeView.as_view(), name='supporttools_home'),
]
