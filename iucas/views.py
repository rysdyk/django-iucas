from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings

def iucas_validate(request):
    user = authenticate(ticket=request.GET["casticket"],casurl=request.build_absolute_uri())
    redirect_url = request.GET["next"]
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            pass
    else:
        messages.error(request, settings.CAS_NOT_REGISTERED_MSG)
    return HttpResponseRedirect(redirect_url)
