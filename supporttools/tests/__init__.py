# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.urls import reverse
from django.test.client import RequestFactory
from userservice.user import UserServiceMiddleware
import mock


def get_request():
    """
    mock request with UserServiceMiddleware initialization
    """
    get_response = mock.MagicMock()
    now_request = RequestFactory().get(reverse('supporttools_home'))
    now_request.session = {}
    UserServiceMiddleware(get_response).process_request(now_request)
    return now_request
