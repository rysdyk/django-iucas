"""
Utility Methods for Authenticating against and using Indiana University CAS.
"""
import httplib2
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def validate_cas_ticket(casticket, casurl):
    """
    Takes a CAS Ticket and makes the out of bound GET request to 
    cas.iu.edu to verify the ticket.
    """
    validate_url = 'https://cas.iu.edu/cas/validate?cassvc=IU&casurl=%s&casticket=%s' %    (casurl,casticket)
    h = httplib2.Http()
    resp, content = h.request(validate_url,"GET")
    return content.splitlines()

    
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
