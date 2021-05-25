from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings

def iucas_validate(request):
    # the login link on ktb/templates/ktb/index.html hits an IU 
    # redirect that returns with the casticket as the param
    # see https://kb.iu.edu/d/bfpq

    # the authenicate method comes from this package's utils.py file
    # however, it doesn't need to be imported because it is specified 
    # in AUTHENTICATION_BACKENDS in opal.settings
    user = authenticate(
        ticket=request.GET["ticket"],
        casurl=request.GET["next"] #'https://ktbdbms.iusm.iu.edu/' #request.build_absolute_uri()
    )

    # casurl can include /?next= param

    try:
        redirect_url = request.GET["next"]
    except:
        redirect_url = 'https://ktbdbms.iusm.iu.edu/ktb'
    
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            messages.error(request, ('This user account has been disabled. '
                'Please contant the KTB if this is an error'))
            pass
    else:
        messages.error(request, settings.CAS_NOT_REGISTERED_MSG)
    
    return HttpResponseRedirect(redirect_url)
