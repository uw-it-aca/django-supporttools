# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf.urls import url
from supporttools.views import home

urlpatterns = [
    # for now... make the home view the default landing for
    # /support
    url(r'^', home, name='supporttools_home'),
    # url(r'^', include('status_app.urls')),
    ]
