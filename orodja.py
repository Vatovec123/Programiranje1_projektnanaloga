# Knjižnica za delo s CSV datotekami
import csv

# Knjižnica za delo z JSON datotekami
import json

# Knjižnica za delo z datotečnim sistemom
import os

# Knjižnica, s katero najenostavneje zajamemo spletne strani
import requests

# ...
import sys


def pripravi_imenik(ime_mape, ime_datoteke):
    os.makedirs(ime_mape, exist_ok=True) # Naredi imenik z dano potjo in vse vmesne imenike. Če je exist_ok=True, ne javi napake, če ciljna mapa že obstaja.
    pot = os.path.join(ime_mape, ime_datoteke) # Staknemo poti, pri čemer Python ustrezno "poskrbi" za prava ločila glede na operacijski sistem. Primer: os.path.join('stanovanja-dolenjska/stanovanja-dolenjska-1.html') -> 'stanovanja-dolenjska/stanovanja-dolenjska-1.html'
    return pot


def shrani_spletno_stran(url, ime_mape, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print(f'Shranjujem {url} ...', end='')
        sys.stdout.flush()
        if os.path.isfile(os.path.join(ime_mape,ime_datoteke)) and not vsili_prenos: 
           print('shranjeno že od prej!')
           return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    else:
        pot = pripravi_imenik(ime_mape, ime_datoteke)
        with open(pot, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')


def vsebina_datoteke(ime_mape, ime_datoteke):
    '''Funkcija vrne celotno vsebino datoteke "ime_mape"/"ime_datoteke" kot niz'''
    pot = os.path.join(ime_mape, ime_datoteke)
    with open(pot, encoding='utf-8') as datoteka:
        return datoteka.read()


def zapisi_csv(slovarji, imena_polj,ime_mape, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pot = pripravi_imenik(ime_mape, ime_datoteke)
    with open(pot, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        writer.writerows(slovarji)


def zapisi_json(objekt,ime_mape, ime_datoteke):
    '''Iz danega objekta ustvari JSON datoteko.'''
    pot = pripravi_imenik(ime_mape, ime_datoteke)
    with open(pot, 'w', encoding='utf-8') as json_datoteka:
        json.dump(objekt, json_datoteka, indent=4, ensure_ascii=False)