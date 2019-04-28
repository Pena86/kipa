# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404

from tupa.models import Sarja

def laskeTulokset_adaptor(sarja_id = None):
    '''
    Muutetaan tulostaulukko paremmin luettavaan muotoon.
    Taroitus myöhemmin tehdä koko tuloslaskin uudestaan ja samalla parempi taulun muotoilu
    '''
    sarja = get_object_or_404(Sarja, id = sarja_id)
    tulokset = sarja.laskeTulokset()

    sijoitus = 1

    pisteet = [x[1] for x in tulokset[0][1:]] #Lista kaikista pisteistä, tasapisteiden määritykseen
    mukana = []
    for var in tulokset[0][1:]:
        mukana.append({'vartio' : var[0], 'sijoitus' : sijoitus, 'tasap' : True if pisteet.count(var[1]) > 1 else False, 'pisteet' : var[1], 'tPist' : var[2:]})
        sijoitus += 1

    pisteet = [x[1] for x in tulokset[1]]
    ulkona = []
    for var in tulokset[1]:
        ulkona.append({'vartio' : var[0], 'sijoitus' : sijoitus, 'tasap' : True if pisteet.count(var[1]) > 1 else False, 'pisteet' : var[1], 'tPist' : var[2:]})
        sijoitus += 1


    return {'sarja' : tulokset[0][0][0],
            'tehtavat' : tulokset[0][0][2:],
            'mukana' : mukana,
            'ulkona' : ulkona,}
