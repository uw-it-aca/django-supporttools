from django.conf import settings
from userservice.user import UserService


def supportools_globals(request):
    params = {
        "supporttools_user": UserService().get_original_user(),
        "supporttools_parent_app": getattr(settings,
                                           "SUPPORTTOOLS_PARENT_APP", ""),
        "supporttools_parent_app_url": getattr(settings,
                                               "SUPPORTTOOLS_PARENT_APP_URL",
                                               "/"),
        "supporttools_extra_views": getattr(settings,
                                            "SUPPORTTOOLS_EXTRA_VIEWS", {}),
    }
    return (params)


def has_less_compiled(request):
    """ See if django-compressor is being used to precompile less
    """
    key = getattr(settings, "COMPRESS_PRECOMPILERS", None)
    return {"has_less_compiled": key != ()}
