from django.urls import reverse
from django.test.client import RequestFactory
from userservice.user import UserServiceMiddleware
from django_user_agents.middleware import UserAgentMiddleware


def get_request(user_agent=''):
    """
    mock request with UserServiceMiddleware initialization
    """
    now_request = RequestFactory().get(
        reverse('supporttools_home'), HTTP_USER_AGENT=user_agent)
    now_request.session = {}
    UserServiceMiddleware().process_request(now_request)
    UserAgentMiddleware().process_request(now_request)
    return now_request
