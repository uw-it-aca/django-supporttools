from django.test.client import RequestFactory
from userservice.user import UserServiceMiddleware


def get_request():
    """
    mock request with UserServiceMiddleware initialization
    """
    now_request = RequestFactory().get("/")
    now_request.session = {}
    UserServiceMiddleware().process_request(now_request)
    return now_request
