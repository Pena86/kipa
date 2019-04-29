from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^(?P<kisa_nimi>[^/]+)/tulokset/(?P<sarja_idt>.*)$', views.tulokset, name='tulokset'),
        #url(r'^kayttaja/(?P<user_name>[^/]+)/$', views.kayttajan_tiedot, name='kayttaja'),
]
