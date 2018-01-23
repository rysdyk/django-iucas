from django.conf.urls import url
from iucas import views

urlpatterns = [
# '',
    url(r'^iucas/$', views.iucas_validate, name="iucas_validate"),
]

