from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^(?P<kisa_nimi>[^/]+)/tulokset/$', views.tulokset, name='tulokset'),
        #url(r'^kayttaja/(?P<user_name>[^/]+)/$', views.kayttajan_tiedot, name='kayttaja'),
]
