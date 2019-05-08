# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.http import HttpResponse

from tupa.models import Kisa, Sarja

from utils import laskeTulokset_adaptor, lpk_piiri_tulokset

import re
import time
import csv

def tulokset(request, kisa_nimi = None, muoto = None, sarja_idt = ''):
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

    lpk = True if sarja_idt.lower().find('lpk') != -1 else False
    piiri = True if sarja_idt.lower().find('piiri') != -1 else False
    kaikki = True if sarja_idt.lower().find('kaikki') != -1 else False
    sarja_idt = re.split(r"[^0-9\s]", sarja_idt)

    lpkt, piirit = [[],[]]
    if lpk or piiri or kaikki:
        lpkt, piirit = lpk_piiri_tulokset(kisa_nimi)

    if kaikki:
        sarja_idt.extend([s.id for s in sarjat])
    elif not lpk:
        lpkt = []
    elif not piiri:
        piirit = []

    for id in sarja_idt:
        try:
            # jos annettu id löytyy sarjojen id:itten listasta, lisää sarja tulostauluun
            if int(id) in [s.id for s in sarjat]: tulokset.append(laskeTulokset_adaptor(int(id)))
        except:
            pass

    #if len(tulokset) < 1: tulokset.append(example)

    #print(csv_output_sarja(tulokset[0]))
    #print(csv_output_piiri(kisa, piirit, lpkt))

    return render(request, 'tulosnaytto/tulokset.html',{
            'kisa_nimi': kisa_nimi,
            'kisa' : kisa,
            'sarjat' : sarjat,
            'heading' : 'Tulokset',
            'tulokset' : tulokset,
            'lpk_tulos' : lpkt,
            'piiri_tulos' : piirit,
            },)

def csv_output_sarja(sarja = None):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + sarja['sarja'].kisa.nimi + "_" + sarja['sarja'].nimi + "_" + time.strftime('%Y-%m-%d_%H-%M') + '.csv'.encode('utf-8')

    writer = csv.writer(response, delimiter=str(u';'))
    writer.writerow([sarja['sarja'].kisa.nimi, '', sarja['sarja'].nimi])
    writer.writerow(['', '', time.strftime("%e.%m.%Y %H:%M ", time.localtime()).replace('.0', '.')])

    writer.writerow(['','']) # Riville vain solunvaihto

    writer.writerow(['','Sij.', 'Nro:', 'Vartio:', 'Yht:'] + [t.jarjestysnro for t in sarja['tehtavat']])
    writer.writerow(['','','','',''] + [t.nimi for t in sarja['tehtavat']])
    writer.writerow(['','','','',''] + [t.lyhenne for t in sarja['tehtavat']])

    writer.writerow(['','','','Max-pisteet', sarja['yhtPist']] + [t.maksimipisteet for t in sarja['tehtavat']])

    writer.writerow(['','']) # Riville vain solunvaihto

    for v in sarja['mukana']:
        writer.writerow(['!' if v['tasap'] else '', v['sijoitus'], v['vartio'].nro, v['vartio'].nimi, v['pisteet']] + [t for t in v['tPist']])

    writer.writerow(['','']) # Riville vain solunvaihto

    writer.writerow(['','','Ulkopuolella:'])
    for v in sarja['ulkona']:
        writer.writerow(['!' if v['tasap'] else '', v['sijoitus'], v['vartio'].nro, v['vartio'].nimi, v['pisteet']] + [t for t in v['tPist']])

    # "".encode('utf8') tarvitaan python 2:n csv-writerin kanssa
    writer.writerow(["",""])
    writer.writerow([u"S = syöttämättä".encode('utf8')])
    writer.writerow([u"H = vartion suoritus hylätty".encode('utf8')])
    writer.writerow([u"K = vartio keskeyttänyt".encode('utf8')])
    writer.writerow([u"E = vartio ei ole tehnyt tehtävää".encode('utf8')])
    writer.writerow([u"! = vartion sijaluku laskettu tasapisteissä määräävien perusteella".encode('utf8')])

    return response

def csv_output_piiri(kisa, piiri = None, lpk = None):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + kisa.nimi + '_piiritulokset_' if piiri else '_lippukuntatulokset_' + time.strftime('%Y-%m-%d_%H-%M') + '.csv'.encode('utf-8')

    writer = csv.writer(response, delimiter=str(u';'))
    writer.writerow([kisa.nimi, '', 'Piiritulokset' if piiri else 'Lippukuntatulosket'])
    writer.writerow(['', '', time.strftime('%e.%m.%Y %H:%M ', time.localtime()).replace('.0', '.')])

    writer.writerow(['','']) # Riville vain solunvaihto

    writer.writerow(['Piiritulokset' if piiri else 'Lippukuntatulokset'])
    writer.writerow(['Piiri' if piiri else 'Lippukuntatulosket', 'Pisteet', 'Vartioita'])
    for i in piiri if piiri else lpk:
        writer.writerow([i['nimi'], i['pisteet'], i['vartioita']])

    return response
