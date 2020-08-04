from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^(?P<kisa_nimi>[^/]+)/kartta/$', views.index, name='index'),
        url(r'^(?P<kisa_nimi>[^/]+)/kartta/rasti/$', views.rasti, name='rasti'),
]
