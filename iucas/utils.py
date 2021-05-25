"""
Utility Methods for Authenticating against and using Indiana University CAS.
"""
import httplib2
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


def validate_cas_ticket(ticket, casurl):
    """
    Takes a CAS Ticket and makes the out of bound GET request to
    cas.iu.edu to verify the ticket.

    see: https://kb.iu.edu/d/bfpq#validate

    Be aware: the cas ticket may be validated only once, 
    and within two seconds of being created.
    """
    #validate_url = 'https://%s/cas/validate?cassvc=IU&casurl=%s' % \
    #    (settings.CAS_HOST, casurl,)

    validate_url = 'https://%s/idp/profile/cas/serviceValidate?ticket=%s&service=%s' % \
        (settings.CAS_HOST, ticket, casurl,)

    # print('1' * 30)
    # print(casurl)
    # print('2' * 30)
    # print(validate_url)
    
    if hasattr(settings, 'CAS_HTTP_CERT'):
        h = httplib2.Http(ca_certs=settings.CAS_HTTP_CERT)
    else:
        h = httplib2.Http()
    
    resp, content = h.request(validate_url, "GET")
    
    # content is a bytestring and requires this decode before splitlines()
    return content.decode('utf-8').splitlines()


# def get_cas_username(casticket, casurl):
#     """
#     Validates the given casticket and casurl and returns the username of the
#     logged in user. If the user is not logged in returns None

#     I don't think is being used anymore
#     """
#     resp = validate_cas_ticket(casticket, casurl)
#     if len(resp) == 2 and resp[0] == 'yes':
#         return resp[1]
#     else:
#         return None

class IUCASBackend:
    """
    IUCAS Authentication Backend for Django
    """
    def authenticate(self, request, ticket, casurl):
        resp = validate_cas_ticket(ticket, casurl)
        print('3' * 30)
        print(resp)

        # a success response from validate_cas_ticket will be a list like this:
        # resp = ['<?xml version="1.0" encoding="UTF-8"?>', 
        # '<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas">', 
        # '  <cas:authenticationSuccess>', 
        # '    <cas:user>srysdyk</cas:user>', 
        # '  </cas:authenticationSuccess>', 
        # '</cas:serviceResponse>']

        if 'authenticationSuccess' in resp[2]:
            username = resp[3][resp[3].find('>')+1:resp[3].find('</')]
            
            if not username:
                return None
            
            try:
                user = User.objects.get(username__iexact=username)
            except User.DoesNotExist:
                return username
            
            return user
        
        else:
            return None

    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
