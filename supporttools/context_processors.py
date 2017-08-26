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
    has_less_precompiler = False
    if key is not None and len(key) > 0:
        for entry in key:
            if entry[0] == "text/less":
                has_less_precompiler = True
    return {"has_less_compiled": has_less_precompiler}


def has_google_analytics(request):
    ga_key = getattr(settings, 'GOOGLE_ANALYTICS_KEY', False)
    return {
        'GOOGLE_ANALYTICS_KEY': ga_key,
        'has_google_analytics': ga_key
    }
