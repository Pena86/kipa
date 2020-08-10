# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse

# Create your views here.

def index(request, kisa_nimi=None):
        """
        Kisaratojen hallintasivu
        """

        return render(request, 'route_management/index.html',{
            'kisa_nimi': kisa_nimi,
            'heading' : 'Rata',},)

def rasti(request, kisa_nimi=None):
        """
        Kisan rastien hallinta
        """

        return render(request, 'route_management/rasti.html',{
            'kisa_nimi': kisa_nimi,
            'heading' : 'Rasti',
            'taakse' : {'url' : reverse("index",args=[kisa_nimi]), 'title' : u'Rata' },
            } ,)
