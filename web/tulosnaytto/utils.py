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

    def myIntify(val):
        # int('') returns error, so this is only way aroind it inside listcomprehension
        try:
            return int(val)
        except Exception as e:
            return 0

    return {'sarja' : tulokset[0][0][0],
            'tehtavat' : tulokset[0][0][2:],
            'yhtPist' : sum([myIntify(t.maksimipisteet) for t in tulokset[0][0][2:]]),
            'mukana' : mukana,
            'ulkona' : ulkona,}

def lpk_piiri_tulokset(kisa_nimi = None):
    sarjat = Sarja.objects.filter(kisa__nimi = kisa_nimi)

    lpkt = []
    piirit = []

    for sarja in sarjat:
        piiri_pisteet = 15
        for v in laskeTulokset_adaptor(sarja.id)['mukana']:
            try:
                if any(l['nimi'] == v['vartio'].lippukunta for l in lpkt):
                    for c, l in enumerate(lpkt):
                        if lpkt[c]['nimi'] == v['vartio'].lippukunta:
                            lpkt[c]['pisteet'] += piiri_pisteet
                            lpkt[c]['vartioita'] += 1
                            break
                else:
                    lpkt.append({'nimi' : v['vartio'].lippukunta, 'pisteet' : piiri_pisteet, 'vartioita' : 1})
            except:
                pass

            try:
                if any(l['nimi'] == v['vartio'].piiri for l in piirit):
                    for c, l in enumerate(piirit):
                        if piirit[c]['nimi'] == v['vartio'].piiri:
                            piirit[c]['pisteet'] += piiri_pisteet
                            piirit[c]['vartioita'] += 1
                            break
                else:
                    piirit.append({'nimi' : v['vartio'].piiri, 'pisteet' : piiri_pisteet, 'vartioita' : 1})
            except:
                pass

            if piiri_pisteet > 0:
                piiri_pisteet -= 1

    lpkt = sorted(lpkt, key = lambda k:k['pisteet'], reverse = True)
    piirit = sorted(piirit, key = lambda k:k['pisteet'], reverse = True)

    #print (sarjat)
    return (lpkt, piirit)
