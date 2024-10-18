import os
import requests
import re
import csv

#Najprej poberemo podatke iz spletne strani in jih pretvorimo v surov text

def link_v_text(link):

    try:
        odziv = requests.get(link)
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

def shrani(link, directory, datoteka):
    vsebina = link_v_text(link)
    text_v_datoteko(vsebina, directory, datoteka)


def datoteka_v_niz(directory, datoteka):
    pot = os.path.join(directory, datoteka)
    with open (pot, 'r', encoding='utf-8') as dat:
        text = dat.read()
    return text

def seznam_oglasov(vsebina):
    vzorec = r'<div class="features-wrapper-picture">(*?)<div class="item-classified-actions">'
    return re.findall(vzorec, vsebina, flags=re.DOTALL)

def slovar_pojmov_v_oglasu(oglas):
    tip_hise = re.search(r'class="title"><h2>()<span class="location">', oglas)
    lokacija = re.search(r'<span class="location">()</span></h2>', oglas)
    cena = re.search(r'class="price-label"><!---->()<!---->', oglas)
    povrsina = re.search(r'class="property"><!--[--><!--]--><span class="nb"><!--[-->()<!--]-->', oglas)
    povrsina_parcele = re.search(r'class="property"><!--[-->land  <!--]--><span class="nb"><!--[-->()<!--]-->', oglas)
    st_spalnic = re.search(r'class="nb"><!--[-->()!--]--></span><!--[-->bedrooms<!--]-->', oglas)
    st_kopalnic = re.search(r'class="nb"><!--[-->()<!--]--></span><!--[-->bathroom<!--]-->', oglas)
    agencija = re.search(r'<p class="agency">(.*)</p></div>', oglas)
    if tip_hise == None or lokacija == None or povrsina == None or povrsina_parcele == None:
        return None
    if povrsina_parcele[-1:-3] == 'ha':
        povrsina_parcele = int(povrsina_parcele) * 10000 
    
    return{'tip hise' : tip_hise.group(1), 
           'lokacija' : lokacija.group(1), 
           'cena' : cena.group(1) if cena else 'ni podatka',  
           'površina' : povrsina.group(1), 
           'površina parcele' : povrsina_parcele.group(1),
           'število spalnic' : st_spalnic.group(1),
           'število kopalnic' : st_kopalnic.group(1),
           'agencija' : agencija.group(1) if agencija else 'ni podatka'}



def vsebina_v_seznam_slovarjev_oglasov(datoteka, directory):
    vsebina = datoteka_v_niz(directory, datoteka)
    vsi_bloki = seznam_oglasov(vsebina)
    oglasi = [slovar_pojmov_v_oglasu(blok) for blok in vsi_bloki]
    return[oglas for oglas in oglasi if oglas != None]

def zapis_v_csv(fieldnames, vrstice, directory, datoteka):
    os.makedirs(directory, datoteka)
    pot = os.path.join(directory, datoteka)
    with open(pot, 'w', encoding='utf-8') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=fieldnames)
        writer.writeheader()
        for vrstica in vrstice:
            writer.writerow(vrstica)
    return

def oglasi_v_csv(oglasi, directory, datoteka):
    assert oglasi and (all(i.keys() == oglasi[0].keys() for i in oglasi))
    fieldnames = list(oglasi[0].keys())
    zapis_v_csv(fieldnames, oglasi, directory, datoteka)
    return None




