from django.conf.urls import patterns, url
from iucas import views

urlpatterns = patterns('', 
    url(r'^iucas/$', views.iucas_validate, name="iucas_validate"),
)

