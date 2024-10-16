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
    vzorec = r'<span class="font-roboto">.*?<img class="logo"'
    return re.findall(vzorec, vsebina, flags=re.DOTALL)

def slovar_pojmov_v_oglasu(oglas):
    lokacija = re.search(r'', oglas)
    cena = re.search(r'', oglas)
    povrsina = re.search(r'', oglas)
    povrsina_parcele = re.search(r'', oglas)
    leto_izgradnje = re.search(r'', oglas)
    st_nadstropij = re.search(r'', oglas)

def vsebina_v_seznam_slovarjev_oglasov(datoteka, directory):
    vsebina = datoteka_v_niz(directory, datoteka)
    vsi_bloki = seznam_oglasov(vsebina)
    oglasi = [slovar_pojmov_v_oglasu(blok) for blok in vsi_bloki]
    return[oglas for oglas in oglasi if oglas != None]
