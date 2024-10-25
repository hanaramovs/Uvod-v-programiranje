import podatki_urejanje as vzorec


def main(redownload=True):
    for i in range(50):
        link = f'https://properties.lefigaro.com/announces/bastide-real+estate-properties+for+sale-france/?type_bien=6&type_bien=9&type_bien=38&type_bien=37&type_bien=34&prix_max=1000000&surface_terrain_min=200&nb_chambres_min=1&nb_pieces_min=1&page={i + 1}'
        if (redownload):
            vzorec.shrani(link, 'oglasi.html', f'oglasi_{i + 1}.html')
    vsebina = ''
    for i in range(50):
        vsebina += vzorec.datoteka_v_niz('oglasi.html', f'oglasi_{i + 1}.html')
    oglasi = vzorec.seznam_oglasov(vsebina)
    seznam = [vzorec.slovar_pojmov_v_oglasu(oglas) for oglas in oglasi]
    vzorec.oglasi_v_csv(seznam, 'projektna_naloga_nepremicnine', 'oglasi.csv')

if __name__ == '__main__':
    main()
