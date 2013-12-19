This is a Django Authentication module that utilizes the Indiana University
CAS System.  Information for integrating with IU CAS is available here:
http://kb.iu.edu/data/atfc.html

## Quick Start

Make sure the iucas is on your python path, either by including the directory
or installing this module with pip or easy_install.

Add 'iucas' to the installed apps in settings.py:

    INSTALLED_APPS = (
        '...',
        'iucas',
    )

Add the iucas to the django auth backends, you may have to add this
section to your settings.py.  You can keep or remove the django model
backend depending on if you want to use both or just IU CAS.

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'iucas.IUCASBackend',
    )

In your login_required decorators and other auth hooks you can now send 
and unauthenticated login link as follows, replacing the casurl with the 
reverse('iucas_validate') link for your setup and the next parameter set 
to the page to redirect back to after login.

    https://cas.iu.edu/cas/login?cassvc=IU&casurl=http://localhost:8000/iucas/iucas?next=/admin
