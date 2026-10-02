def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    album = {}                          #creo l'album vuoto

    try:
        infile = open(file_path, "r")   #apro file
        infile.readline()               #salto intestazione

        for line in infile:              #leggo tutte le righe del file
            line = line.rstrip()          #per ogni riga elimina i caratteri bianchi finali

            if line == "":               #evito che mi dia errore se una riga è vuota
                continue                   # (se è vuota passa alla prossima senza eseguire i comandi)

            dati = line.split(",")       #ogni riga viene trasformata in una lista
            codice = dati[0].strip()     #per ogni riga in base alla posizione dell'elemnto, questo viene categorizzato
            titolo = dati[1].strip()
            autore = dati[2].strip()
            mese = int(dati[3])
            anno = int(dati[4])

            if anno not in album:         # se l'anno non esiste, crea il dizionario interno
                album[anno] = {}

            album[anno][codice] = [titolo, autore, mese]       #ogni foto viene aggiunta al dizionario, contenuto
                                                               # nell'album, riferito all'anno in cui è stata scattata

        infile.close()                    #chiudo il file

    except FileNotFoundError:             #se non viene trovato un file, il programma restituisce None
        return None

    return album                          #se il file viene trovato e le istruzioni vengono eseguite correttamente,
                                          #il programma restituisce l'album contenente tutte le foto del file


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    if mese < 1 or mese > 12:      #controllo che il mese inserito esista
        return None

    if cerca_foto(album, codice) is not None:     #controllo che la foto non sia già presente nell'album
        return None

    foto = [titolo, autore, mese]                 #creo lista contenente le informazioni della nuova foto

    try:                                          #provo a eseguire i comandi, controllando se si presenta un errore
        infile = open(file_path, "r+")            #apre nuovamente il file in modalità lettura e scrittura
        contenuto = infile.read()                 #legge tutto il file fino alla fine

        if contenuto != "" and not contenuto.endswith("\n"):      #se il nuovo file aggiornato non finisce con una riga
            infile.write("\n")                                    #vuota o con un a capo, lo aggiunge

        infile.write(f"{codice},{titolo},{autore},{mese},{anno}\n")        #scrive sul file esistente la nuova foto

        infile.close()         #chiudo il file

    except OSError:            #se il file non viene trovato la funzione ritorna None
        return None

    if anno not in album:          #controllo se l'anno in cui è stata scattata la nuova foto è già presente nell'album
        album[anno] = {}           #se non è presente creo un dizionario all'interno dell'album che abbia come chiave
                                   #l'anno in cui è stata scattata

    album[anno][codice] = foto        #aggiungo la foto al dizionario che ha come chiave
                                                        # l'anno in cui è stata scattata

    return foto                    #se tutti i comandi sono stati eseguiti correttamente e non sono stati rilevati
                                   # errori la funzione ritorna un riferimento alla foto aggiunta


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for anno in album:                       # cerca l'anno della foto che ci interessa nell'album
        if codice in album[anno]:            #cerca il codice della foto nel dizionario riferito all'anno della foto
            foto = album[anno][codice]       #trova la foto e crea la variabile contente le informazioni della foto

            titolo = foto[0]                 #ogni informazione della foto viene categorizzata
            autore = foto[1]
            mese = foto[2]

            return f"{codice}, {titolo}, {autore}, {mese}, {anno}"    #la funzione ritorna le informazioni della foto

    return None                              #se la foto non è stata trovata la funzione ritorna None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    if anno not in album:                    #se nell'anno d'interesse non sono state scattate foto, la funzione
        return None                          #ritorna None

    titoli = []                              #se l'anno è presente nell'album viene creata una lista che conterrà
                                             #tutte le foto scattate in quell'anno
    for codice in album[anno]:
        foto = album[anno][codice]           #il titolo di ogni foto scattata in quell'anno viene aggiunta
        titoli.append(foto[0])               # alla lista creata prima

    titoli.sort()                            #la lista dei titoli viene ordinata in ordine alfabetico

    return titoli                            #la funzione ritona la lista dei titoli delle foto scattate in quell'anno


def main():
    album = {}
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                print(album)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
