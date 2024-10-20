import os
import requests
import re
import csv

#Najprej poberemo podatke iz spletne strani in jih pretvorimo v surov text

def link_v_text(link):
    try:
        headers = {"User-agent" : "Chrome/111.05563.111"}
        odziv = requests.get(link, headers=headers)
    except requests.exceptions.RequestException:
        print ('prišlo je do napake pri spletni strani')
        return None 
    return odziv.text

#Nato text prepišemo v datoteko 
def text_v_datoteko(text, directory, datoteka):
    os.makedirs(directory, exist_ok=True)
    pot = os.path.join(directory, datoteka)
    with open(pot, 'w', encoding='utf-8') as izvozna_datoteka:
        izvozna_datoteka.write(text)
    return None

def shrani(odziv, directory, datoteka):
    vsebina = link_v_text(odziv)
    text_v_datoteko(vsebina, directory, datoteka)


def datoteka_v_niz(directory, datoteka):
    pot = os.path.join(directory, datoteka)
    with open (pot, 'r', encoding='utf-8') as dat:
        vsebina = dat.read().replace('\n', ' ')
    return vsebina

def seznam_oglasov(vsebina):
    vzorec = r'<div class="features-wrapper-picture">.*?<div class="item-classified-actions">'
    return re.findall(vzorec, vsebina, flags=re.DOTALL)

def slovar_pojmov_v_oglasu(oglas):
    tip_hise = re.search(r'class="title"><h2>(.*)<span class="location">', oglas) #dela
    lokacija = re.search(r'<span class="location">(.*)</span></h2>', oglas) #dela
    cena = re.search(r'class="price-label"><!\-\-\-\->(.*) <!\-\-\-\->', oglas) #dela
    povrsina = re.search(r'class="property"><!\-\-\[\-\-><!\-\-\]\-\-><span class="nb"><!\-\-\[\-\->(.*)<!\-\-\]\-\-></span><!\-\-\[\-\->m²<!\-\-\]\-\-></div><!\-\-\-\-><div class="property">', oglas)#dela
    povrsina_parcele = re.search(r'class="property"><!\-\-\[\-\->land  <!\-\-\]\-\-><span class="nb"><!\-\-\[\-\->(.*)<!\-\-\]\-\-></span><!\-\-\[\-\->(m²|ha)<!\-\-\]\-\-></div>', oglas)
    st_spalnic = re.search(r'class="nb"><!\-\-\[\-\->(\d*)<!\-\-\]\-\-></span><!\-\-\[\-\->bedrooms<!\-\-\]\-\->', oglas)#dela
    st_kopalnic = re.search(r'class="nb"><!\-\-\[\-\->(\d*)<!\-\-\]\-\-></span><!\-\-\[\-\->bathroom<!\-\-\]\-\->', oglas)#dela
    agencija = re.search(r'<p class="agency">(.*)</p></div>', oglas) #dela

    # merska_enota_parcele = str(povrsina_parcele.group(2).replace(',', ''))
    # if merska_enota_parcele == 'ha':
    #     koncna_povrsina_parcele = float(povrsina_parcele.group(1).replace(',', '')) * 10000
    # else:
    #     koncna_povrsina_parcele = float(povrsina_parcele.group(1).replace(',', ''))
    #     return None
    
    return{'tip hise' : tip_hise.group(1).strip(), 
           'lokacija' : lokacija.group(1),
           'cena' : int(cena.group(1).strip().lstrip('$').replace(',', '')) if cena else 'ni podatka o ceni',
           'površina' : int(povrsina.group(1).replace(',', '')) if povrsina else 'ni podatka2',
           'površina parcele' : (povrsina_parcele.group(1).replace(',', '')) if povrsina_parcele else 'ni podatka3',
           'merska enota parcele' : (povrsina_parcele.group(2)) if povrsina_parcele else 'ni podatka3',
           'število spalnic' : st_spalnic.group(1) if st_spalnic else 'ni spalnic',
           'število kopalnic' : st_kopalnic.group(1) if st_kopalnic else 'ni kopalnic',
           'agencija' : agencija.group(1) if agencija else 'ni podatka_o_agenciji'}

def vsebina_v_seznam_slovarjev_oglasov(datoteka, directory):
    vsebina = datoteka_v_niz(directory, datoteka)
    vsi_bloki = seznam_oglasov(vsebina)
    oglasi = [slovar_pojmov_v_oglasu(oglas) for oglas in vsi_bloki]
    return[oglas for oglas in oglasi if oglas != None]

def zapis_v_csv(fieldnames, vrstice, directory, datoteka):
    os.makedirs(directory, exist_ok=True)
    pot = os.path.join(directory, datoteka)
    with open(pot, 'w', encoding='utf-8') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=fieldnames)
        writer.writeheader()
        for vrstica in vrstice:
            writer.writerow(vrstica)
    return

def oglasi_v_csv(oglasi, directory, datoteka):
    fieldnames = list(oglasi[0].keys())
    zapis_v_csv(fieldnames, oglasi, directory, datoteka)
    return None
