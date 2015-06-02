"""
Utility Methods for Authenticating against and using Indiana University CAS.
"""
import httplib2
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

def validate_cas_ticket(casticket, casurl):
    """
    Takes a CAS Ticket and makes the out of bound GET request to 
    cas.iu.edu to verify the ticket.
    """
    validate_url = 'https://%s/cas/validate?cassvc=IU&casurl=%s' % \
        (settings.CAS_HOST, casurl,)
    if hasattr(settings, 'CAS_HTTP_CERT'):
        h = httplib2.Http(ca_certs=settings.CAS_HTTP_CERT)
    else:
        h = httplib2.Http() 
    resp, content = h.request(validate_url,"GET")
    return content.splitlines()


def get_cas_username(casticket, casurl):
    """
    Validates the given casticket and casurl and returns the username of the
    logged in user. If the user is not logged in returns None 
    """
    resp = validate_cas_ticket(casticket, casurl)
    if len(resp) == 2 and resp[0] == 'yes':
        return resp[1]
    else:
        return None
    
class IUCASBackend(object):
    """
    IUCAS Authentication Backend for Django
    """
    def authenticate(self, ticket, casurl):
        resp = validate_cas_ticket(ticket, casurl)
        if len(resp) == 2 and resp[0] == 'yes':
            username = resp[1]
            if not username:
                return None
            try: 
                user = User.objects.get(username__iexact=username)
            except User.DoesNotExist: 
                return None
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
