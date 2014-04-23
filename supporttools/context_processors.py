""" context_processors.py

To make this available in your RequestContext() add

'supporttools.context_processors.global_supportools_stuff'

to yourTEMPLATE_CONTEXT_PROCESSORS setting.
"""
from django.conf import settings
from userservice.user import UserService

def supportools_globals(request):
    
    # WARNING... THIS IS NOT PRODUCTION CODE!
    user_service = UserService()
    
    params = {
        'supporttools_parent_app' : settings.SUPPORTTOOLS_PARENT_APP,
        'supporttools_user' : user_service.get_original_user(),
        'supporttools_is_overrideable' : settings.SUPPORTTOOLS_IS_OVERRIDEABLE,
    }
    
    return (params)
    
    
