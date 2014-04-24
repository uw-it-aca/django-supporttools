from django.conf import settings
from userservice.user import UserService


def supportools_globals(request):
    user_service = UserService()
    params = {
        "supporttools_parent_app": getattr(settings, "SUPPORTTOOLS_PARENT_APP", ""),
        "supporttools_user": user_service.get_original_user(),
    }
    return (params)


def has_less_compiled(request):
    """ See if django-compressor is being used to precompile less
    """ 
    key = getattr(settings, "COMPRESS_PRECOMPILERS", None)
    return {'has_less_compiled': key != ()}
