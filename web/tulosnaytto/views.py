# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib import messages

def tulokset(request, kisa_nimi=None):
    tulokset = {
           'sarja' : 'Oranssi',
           'tehtavat' : [
                        {'num' : 1, 'nimi' : 'pah', 'pist' : 4},
                        {'num' : 2, 'nimi' : 'vies', 'pist' : 5},
                        {'num' : 3, 'nimi' : 'gran', 'pist' : 3},
                        {'num' : 4, 'nimi' : 'nayt', 'pist' : 5},
                        {'num' : 5, 'nimi' : 'laiv', 'pist' : 5},
                        ],
           'yhtPist' : 52,
           'vartiot' : [
                       {'nimi' : 'a', 'numero' : 101, 'lpk' : 'a', 'piiri' : 'a', 'sijoitus' : 1, 'tasap' : False, 'pisteet' : 31.3, 'tPist' : [2.5, 2.6, 3.0, 3.0, 3.0]},
                       {'nimi' : 'b', 'numero' : 102, 'lpk' : 'b', 'piiri' : 'b', 'sijoitus' : 2, 'tasap' : True, 'pisteet' : 25.0, 'tPist' : [0.6, 4.0, 0.0, 2.5, 1.5]},
                       {'nimi' : 'c', 'numero' : 103, 'lpk' : 'c', 'piiri' : 'c', 'sijoitus' : 3, 'tasap' : False, 'pisteet' : 22.8, 'tPist' : [1.6, 2.7, 2.1, 3.5, 4.5]},
                       ],
           }
    return render(request, 'tulosnaytto/tulokset.html',{
            'kisa_nimi': kisa_nimi,
            'heading' : 'Tulokset',
            'tulokset' : tulokset,
            },)
