import orodja

#Knjižnica za delo z regularnimi izrazi.
import re

import requests


regije =[
    "ljubljana-mesto",
    "ljubljana-okolica",
    "gorenjska",
    "juzna-primorska",
    "severna-primorska",
    "notranjska",
    "savinjska",
    "podravska",
    "koroska",
    "dolenjska",
    "posavska",
    "zasavska",    
    "pomurska"
]



def poisci_oglas(vsebina):
    """Funkcija poišče posamezne oglase, ki se nahajajo v spletni strani in
    vrne seznam oglasov."""
    rx = re.compile(r'<meta itemprop="category".*?<meta itemprop="priceCurrency" content="EUR" />', re.DOTALL)
    oglasi = re.findall(rx,vsebina)  # Seznam nizov
    return oglasi


vzorec_stanovanja = re.compile(
    r'<span class="title">(?P<Ime>.*?)</span></a></h2>.*?'
    r'</span><span class="atribut leto">Leto: <strong>(?P<Leto>.*?)</strong>.*?'
    r'<span class="velikost" lang="sl">(?P<Velikost>.*?) m2</span><br />.*?'
    r'<span class="cena">(?P<Cena>.*?) &euro.*?',
    re.DOTALL)



def podatki_stanovanja(blok, regija):
    stanovanje = vzorec_stanovanja.search(blok).groupdict()
    stanovanje['Leto'] = int(stanovanje['Leto'])
    stanovanje['Velikost'] = float(stanovanje['Velikost'].replace('.', '').replace(',', '.'))
    stanovanje['Cena'] = float(stanovanje['Cena'].replace('.', '').replace(',', '.'))
    stanovanje['Regija'] = regija
    return stanovanje



stanovanja = []
for regija in regije:
    # mapa v katero bomo shranili datoteke
    ime_mape = f'stanovanja-{regija}'
    for stran in range(1,37): 
        url = f'https://www.nepremicnine.net/oglasi-prodaja/{regija}/stanovanje/{stran}/'
        datoteka = f'stanovanja-{regija}-{stran}.html'
        orodja.shrani_spletno_stran(url, ime_mape, datoteka)
        vsebina = orodja.vsebina_datoteke(ime_mape, datoteka)
        
        oglasi = poisci_oglas(vsebina)
        for oglas in oglasi:
           podatek = podatki_stanovanja(oglas, regija)
           stanovanja.append(podatek)
print(len(stanovanja)) # Izbriši
orodja.zapisi_json(stanovanja, 'obdelani-podatki','stanovanja.json')
orodja.zapisi_csv(
    stanovanja,
    ['Ime','Leto', 'Velikost', 'Cena', 'Regija'], 'obdelani-podatki','stanovanja.csv'
)



  




    

