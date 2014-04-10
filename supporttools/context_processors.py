""" context_processors.py

To make this available in your RequestContext() add

'supporttools.context_processors.global_supportools_stuff'

to yourTEMPLATE_CONTEXT_PROCESSORS setting.
"""
from django.conf import settings

from restclients.pws import PWS
from userservice.user import UserService

def global_supportools_stuff(request):
    
    # WARNING... THIS IS NOT PRODUCTION CODE!
    user_service = UserService()
    user = PWS().get_person_by_netid(user_service.get_original_user())
    
    params = {
        'supporttools_parent_app' : settings.SUPPORTTOOLS_PARENT_APP,
        'supporttools_user': user.uwnetid,
    }
    
    print "global_supporttools processor just ran!"

    return (params)
    
    
