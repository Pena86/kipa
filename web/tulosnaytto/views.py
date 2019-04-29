# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.contrib import messages

from tupa.models import Kisa, Sarja

from utils import laskeTulokset_adaptor

import re

def tulokset(request, kisa_nimi = None, sarja_idt = None):
    example = {
           'sarja' : {'nimi' : 'Oranssi'},
           'tehtavat' : [
                        {'jarjestysnro' : 1, 'nimi' : 'pah', 'maksimipisteet' : 4},
                        {'jarjestysnro' : 2, 'nimi' : 'vies', 'maksimipisteet' : 5},
                        {'jarjestysnro' : 3, 'nimi' : 'gran', 'maksimipisteet' : 3},
                        {'jarjestysnro' : 4, 'nimi' : 'nayt', 'maksimipisteet' : 5},
                        {'jarjestysnro' : 5, 'nimi' : 'laiv', 'maksimipisteet' : 5},
                        ],
           'yhtPist' : 52,
           'mukana' : [
                       {'vartio' : {'nimi' : 'a', 'nro' : 101, 'lpk' : 'a', 'piiri' : 'a'}, 'sijoitus' : 1, 'tasap' : False, 'pisteet' : 31.3, 'tPist' : [2.5, 2.6, 3.0, 3.0, 3.0]},
                       {'vartio' : {'nimi' : 'b', 'nro' : 102, 'lpk' : 'b', 'piiri' : 'b'}, 'sijoitus' : 2, 'tasap' : True, 'pisteet' : 25.0, 'tPist' : [0.6, 4.0, 0.0, 2.5, 1.5]},
                       {'vartio' : {'nimi' : 'c', 'nro' : 103, 'lpk' : 'c', 'piiri' : 'c'}, 'sijoitus' : 3, 'tasap' : False, 'pisteet' : 22.8, 'tPist' : [1.6, 2.7, 2.1, 3.5, 4.5]},
                       ],
           'ulkona' : [
                       {'vartio' : {'nimi' : 'a', 'nro' : 101, 'lpk' : 'a', 'piiri' : 'a'}, 'sijoitus' : 1, 'tasap' : False, 'pisteet' : 31.3, 'tPist' : [2.5, 2.6, 3.0, 3.0, 3.0]},
                       {'vartio' : {'nimi' : 'a', 'nro' : 101, 'lpk' : 'a', 'piiri' : 'a'}, 'sijoitus' : 1, 'tasap' : False, 'pisteet' : 31.3, 'tPist' : [2.5, 2.6, 3.0, 3.0, 3.0]},
                      ],
           }

    kisa = get_object_or_404(Kisa, nimi = kisa_nimi)
    sarjat = Sarja.objects.filter(kisa__nimi = kisa_nimi)
    tulokset = []

    print (sarja_idt, re.split(r"[^0-9\s]", sarja_idt))
    for id in re.split(r"[^0-9\s]", sarja_idt):
        try:
            # jos annettu id löytyy sarjojen id:itten listasta, lisää sarja tulostauluun
            if int(id) in [s.id for s in sarjat]: tulokset.append(laskeTulokset_adaptor(int(id)))
        except:
            pass

    #if len(tulokset) < 1: tulokset.append(example)

    return render(request, 'tulosnaytto/tulokset.html',{
            'kisa_nimi': kisa_nimi,
            'kisa' : kisa,
            'sarjat' : sarjat,
            'heading' : 'Tulokset',
            'tulokset' : tulokset,
            },)
