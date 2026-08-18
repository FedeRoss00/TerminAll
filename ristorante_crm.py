"""
Modulo per la gestione del CRM di un ristorante.
Consente di gestire il menù, i tavoli, gli ordini e i pagamenti.
"""

"""Richiede il modulo datetime per gestire le date e gli orari degli ordini."""
from datetime import datetime
"""Richiede il modulo database per gestire il caricamento e l'inizializzazione del database dei piatti."""
import database_ristorante as database

database.inizializza_database()

menu_piatti = database.carica_piatti()
tavoli = database.carica_tavoli()
storico_pagamenti = database.carica_storico()

"""Definisco le funzioni principali per la gestione del CRM del ristorante, tra cui la visualizzazione del menù, la gestione dei tavoli, la creazione di nuovi ordini, il pagamento e la visualizzazione dello storico degli ordini."""
def mostra_menu():
    print("\n" + "=" * 40)
    print("Benvenuto nel CRM del ristorante! 🍽️")
    print("=" * 40)
    print("0. Esci ❌")
    print("1. Gestione Menù 🍽️")
    print("2. Gestione Tavoli 🪑")
    print("3. Nuovo Ordine 📝")
    print("4. Pagamento 💳")
    print("5. Storico Ordini 📜")
    print("=" * 40)

"""Definisco la funzione per visualizzare i piatti del menù, aggiungere nuovi piatti e rimuovere piatti esistenti."""
def visualizza_piatti():
    print("\n" + "-" * 40)
    print("Piatti del Menù 🍽️")
    print("-" * 40)
    if not menu_piatti:
        print("Il menù è vuoto. Aggiungi dei piatti con l'opzione 2 per visualizzarli.")
        return
    """Gestisco la visualizzazione dei piatti del menù, mostrando il nome e il prezzo di ciascun piatto."""
    for indice, piatto in enumerate(menu_piatti, start=1):
        print(f"{indice}. {piatto['nome']} - Prezzo: {piatto['prezzo']}€")

"""Funzione per aggiungere un nuovo piatto al menù, richiedendo all'utente il nome e il prezzo del piatto."""
def aggiungi_piatto():
    nome = input("Inserisci il nome del piatto (0 per annullare): ")
    if nome == "0":
        return
    prezzo = input("Inserisci il prezzo del piatto: ")
    try:
        prezzo = float(prezzo)
    except ValueError:
        print("Prezzo non valido. Assicurati di inserire un numero. Riprova. 🚫")
        return
    nuovo_id = database.salva_piatto(nome, prezzo)
    nuovo_piatto = {"id": nuovo_id, "nome": nome, "prezzo": prezzo}
    menu_piatti.append(nuovo_piatto)
    print(f"Piatto '{nome}' aggiunto al menù con successo. ✅")

"""Funzione per rimuovere un piatto dal menù, mostrando all'utente l'elenco dei piatti e richiedendo il numero del piatto da rimuovere."""
def rimuovi_piatto():
    visualizza_piatti()
    if not menu_piatti:
        return
    scelta = input("Inserisci il numero del piatto da rimuovere (0 per annullare): ")
    if scelta == "0":
        return
    try:
        indice = int(scelta) - 1
    except ValueError:
        print("Inserisci un numero valido.")
        return
    if 0 <= indice < len(menu_piatti):
        piatto_rimosso = menu_piatti.pop(indice)
        database.elimina_piatto(piatto_rimosso["id"])
        print(f"Piatto '{piatto_rimosso['nome']}' rimosso dal menù con successo. ✅")
    else:
        print("Scelta non valida. Riprova. 🚫")

"""Funzione per gestire il menù del ristorante, consentendo all'utente di visualizzare i piatti, aggiungere nuovi piatti o rimuovere piatti esistenti."""
def gestione_menu():
    while True:
        print("\n" + "-" * 40)
        print("Gestione Menù 🍽️")
        print("-" * 40)
        print("1. Visualizza Piatti")
        print("2. Aggiungi Piatto")
        print("3. Rimuovi Piatto")
        print("0. Torna al menu principale 🔙")
        print("-" * 40)
        scelta = input("Scegli un'opzione: ")

        if scelta == "1":
            visualizza_piatti()
        elif scelta == "2":
            aggiungi_piatto()
        elif scelta == "3":
            rimuovi_piatto()
        elif scelta == "0":
            break
        else:
            print("Scelta non valida. Riprova. 🚫")

"""Funzione per impostare il numero di tavoli nel ristorante, richiedendo all'utente di inserire un numero valido e creando una lista di tavoli con ordini vuoti."""
def imposta_numero_tavoli():
    numero_tavoli = input("Inserisci il numero di tavoli nel ristorante: ")
    try:
        numero_tavoli = int(numero_tavoli)
        if numero_tavoli <= 0:
            print("Il numero di tavoli deve essere maggiore di zero. Riprova. 🚫")
            return
    except ValueError:
        print("Inserisci un numero valido. Riprova. 🚫")
        return
    """Imposto il numero di tavoli nel ristorante, creando una lista di dizionari per ciascun tavolo con un numero identificativo e una lista vuota di ordini."""
    tavoli.clear()
    """Ciclo per creare i tavoli, assegnando a ciascun tavolo un numero identificativo e una lista vuota di ordini."""
    for i in range(1, numero_tavoli + 1):
        tavoli.append({"numero": i, "ordini": []})
    database.salva_numero_tavoli(numero_tavoli)
    print(f"{numero_tavoli} tavoli creati con successo. ✅")

"""Funzione per visualizzare lo stato dei tavoli nel ristorante. Inoltra, mostra gli ordini associati a ciascun tavolo e il totale parziale degli ordini."""
def visualizza_tavoli():
    if not tavoli:
        print("Non hai ancora impostato i tavoli. Usa l'opzione 1.")
        return

    print("\n" + "-" * 40)
    print("Situazione Tavoli")
    print("-" * 40)
    for tavolo in tavoli:
        print(f"\nTavolo {tavolo['numero']}:")
        if not tavolo["ordini"]:
            print("  Nessun ordine.")
            continue
        totale = calcola_totale_tavolo(tavolo)
        for piatto in tavolo["ordini"]:
            print(f"  - {piatto['nome']} ({piatto['prezzo']}€)")
        print(f"  Totale parziale: {totale}€")
"""Funzione per consentire all'utente di scegliere un tavolo esistente, restituendo il dizionario del tavolo selezionato o None se l'utente annulla la scelta o inserisce un numero non valido."""
def scegli_tavolo():
    numero_test = input("Inserisci il numero del tavolo (0 per annullare): ")
    if numero_test == "0":
        return None
    try:
        numero_tavolo = int(numero_test)
    except ValueError:
        print("Inserisci un numero valido. Riprova. 🚫")
        return None
    for tavolo in tavoli:
        if tavolo["numero"] == numero_tavolo:
            return tavolo
    print("Tavolo non trovato. Riprova. 🚫")
    return None
"""Funzione per assegnare un piatto a un tavolo, richiedendo all'utente di scegliere un tavolo esistente e un piatto dal menù. Aggiunge il piatto selezionato alla lista degli ordini del tavolo e stampa un messaggio di conferma."""
def assegna_piatto_a_tavolo():
    if not tavoli:
        print("Non hai ancora impostato i tavoli. Usa l'opzione 1.")
        return
    if not menu_piatti:
        print("Il menù è vuoto. Aggiungi dei piatti con l'opzione 2 per poterli assegnare ai tavoli.")
        return
    tavolo = scegli_tavolo()
    if tavolo is None:
        return
    visualizza_piatti()
    scelta = input("Inserisci il numero del piatto da assegnare al tavolo (0 per annullare): ")
    if scelta == "0":
        return
    try:
        indice = int(scelta) - 1
    except ValueError:
        print("Inserisci un numero valido. Riprova. 🚫")
        return
    if 0 <= indice < len(menu_piatti):
        piatto_scelto = menu_piatti[indice]
        id_ordine = database.salva_ordine_tavolo(tavolo["numero"], piatto_scelto["nome"], piatto_scelto["prezzo"])
        piatto_ordinato = {"id_ordine": id_ordine, "nome": piatto_scelto["nome"], "prezzo": piatto_scelto["prezzo"]}
        tavolo["ordini"].append(piatto_ordinato)
        print(f"Piatto '{piatto_scelto['nome']}' assegnato al Tavolo {tavolo['numero']} con successo. ✅")
    else:
        print("Scelta non valida. Riprova. 🚫")

"""Funzione per rimuovere un piatto da un tavolo, richiedendo all'utente di scegliere un tavolo esistente e il piatto da rimuovere. Aggiorna la lista degli ordini del tavolo e stampa un messaggio di conferma."""
def rimuovi_piatto_da_tavolo():
    if not tavoli:
        print("Non hai ancora impostato i tavoli. Usa l'opzione 1.")
        return
    tavolo = scegli_tavolo()
    if tavolo is None:
        return
    if not tavolo["ordini"]:
        print(f"Il Tavolo {tavolo['numero']} non ha ordinato piatti.")
        return
    print(f"\nOrdini del Tavolo {tavolo['numero']}:")
    """Ciclo per visualizzare gli ordini del tavolo selezionato, mostrando il nome e il prezzo di ciascun piatto. L'utente può scegliere il numero del piatto da rimuovere o annullare l'operazione inserendo 0."""
    for indice, piatto in enumerate(tavolo["ordini"], start=1):
        print(f"{indice}. {piatto['nome']} ({piatto['prezzo']}€)")
    scelta = input("Inserisci il numero del piatto da rimuovere (0 per annullare): ")
    if scelta == "0":
        return
    try:
        indice = int(scelta) - 1
    except ValueError:
        print("Inserisci un numero valido. Riprova. 🚫")
        return
    if 0 <= indice < len(tavolo["ordini"]):
        piatto_rimosso = tavolo["ordini"].pop(indice)
        database.elimina_ordine_tavolo(piatto_rimosso["id_ordine"])
        print(f"Piatto '{piatto_rimosso['nome']}' rimosso dall'ordine del Tavolo {tavolo['numero']} con successo. ✅")
    else:
        print("Scelta non valida. Riprova. 🚫")
"""Funzione per gestire i tavoli del ristorante, consentendo all'utente di impostare il numero di tavoli, visualizzare lo stato dei tavoli e degli ordini, assegnare piatti ai tavoli e rimuovere piatti dai tavoli."""
def gestione_tavoli():
    while True:
        print("\n" + "-" * 40)
        print("Gestione Tavoli 🍽️")
        print("-" * 40)
        print("1. Imposta Numero di Tavoli")
        print("2. Visualizza Tavoli e Ordini")
        print("3. Assegna Piatto a Tavolo")
        print("4. Rimuovi Piatto da Tavolo")
        print("0. Torna al menu principale 🔙")
        print("-" * 40)
        scelta = input("Scegli un'opzione: ")

        if scelta == "1":
            imposta_numero_tavoli()
        elif scelta == "2":
            visualizza_tavoli()
        elif scelta == "3":
            assegna_piatto_a_tavolo()
        elif scelta == "4":
            rimuovi_piatto_da_tavolo()
        elif scelta == "0":
            break
        else:
            print("Scelta non valida. Riprova. 🚫")
            
"""Funzione per creare un nuovo ordine per un tavolo, consentendo all'utente di scegliere un tavolo esistente e aggiungere piatti dal menù all'ordine del tavolo. Alla fine, stampa un messaggio di conferma con il numero di piatti aggiunti all'ordine."""
def nuovo_ordine():
    if not tavoli:
        print("Non hai ancora impostato i tavoli. Usa l'opzione 1.")
        return
    if not menu_piatti:
        print("Il menù è vuoto. Aggiungi dei piatti con l'opzione 2 per poterli ordinare.")
        return
    tavolo = scegli_tavolo()
    if tavolo is None:
        return
    print(f"\nNuovo Ordine per il Tavolo {tavolo['numero']}:")
    piatti_aggiunti = 0
    while True:
        visualizza_piatti()
        scelta = input("Inserisci il numero del piatto da aggiungere all'ordine (0 per terminare): ")
        if scelta == "0":
            break
        try:
            indice = int(scelta) - 1
        except ValueError:
            print("Inserisci un numero valido. Riprova. 🚫")
            continue
        if 0 <= indice < len(menu_piatti):
            piatto_scelto = menu_piatti[indice]
            id_ordine = database.salva_ordine_tavolo(tavolo["numero"], piatto_scelto["nome"], piatto_scelto["prezzo"])
            piatto_ordinato = {"id_ordine": id_ordine, "nome": piatto_scelto["nome"], "prezzo": piatto_scelto["prezzo"]}
            tavolo["ordini"].append(piatto_ordinato)
            piatti_aggiunti += 1
            print(f"Piatto '{piatto_scelto['nome']}' aggiunto all'ordine del Tavolo {tavolo['numero']}. ✅")
        else:
            print("Scelta non valida. Riprova. 🚫")
    if piatti_aggiunti > 0:
        print(f"Ordine per il Tavolo {tavolo['numero']} completato con {piatti_aggiunti} piatti. ✅")
    else:
        print(f"Nessun piatto aggiunto all'ordine del Tavolo {tavolo['numero']}.")
"""Calcolo del totale degli ordini per un tavolo specifico, sommando i prezzi di tutti i piatti ordinati."""
def calcola_totale_tavolo(tavolo):
    totale = 0
    for piatto in tavolo["ordini"]:
        totale += piatto["prezzo"]
    return totale

"""Gestione del pagamento per un tavolo, consentendo all'utente di scegliere un tavolo esistente, visualizzare gli ordini e il totale da pagare, selezionando il metodo di pagamento e liberando il tavolo."""
def pagamento():
    if not tavoli:
        print("Non hai ancora impostato i tavoli. Usa l'opzione 1.")
        return
    tavolo = scegli_tavolo()
    if tavolo is None:
        return
    if not tavolo["ordini"]:
        print(f"Il Tavolo {tavolo['numero']} non ha ordinato piatti.")
        return
    print(f"\n💵 Pagamento per il Tavolo {tavolo['numero']}:")
    for piatto in tavolo["ordini"]:
        print(f"  - {piatto['nome']} ({piatto['prezzo']}€)")
    totale = calcola_totale_tavolo(tavolo)
    print(f"TOTALE DA PAGARE: {totale:.2f}€")

    print("\nMetodo di pagamento:")
    print("1. Contanti")
    print("2. Carta")
    print("0. Annulla")
    metodo = input("Scegli: ").strip()

    if metodo == "0":
        print("Pagamento annullato.")
        return

    if metodo == "2":
        metodo_display = "Carta"
        print(f"Pagamento con carta di {totale:.2f}€ effettuato. ✅")
    elif metodo == "1":
        metodo_display = "Contanti"
        importo_testo = input(f"Importo consegnato dal cliente (minimo {totale:.2f}€): ").strip()
        importo_testo = importo_testo.replace(",", ".")
        try:
            importo = float(importo_testo)
        except ValueError:
            print("Importo non valido. Pagamento annullato. 🚫")
            return
        if importo < totale:
            mancante = round(totale - importo, 2)
            print(f"Importo insufficiente: mancano ancora {mancante:.2f}€. Pagamento annullato. 🚫")
            return
        resto = round(importo - totale, 2)
        print(f"Contanti ricevuti: {importo:.2f}€")
        if resto > 0:
            print(f"Resto da dare al cliente: {resto:.2f}€")
        else:
            print("Nessun resto da dare.")
    else:
        print("Metodo di pagamento non valido. Pagamento annullato. 🚫")
        return

    data_ora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    database.salva_pagamento(tavolo["numero"], tavolo["ordini"], totale, metodo_display, data_ora)
    storico_pagamenti.append({
        "tavolo": tavolo["numero"],
        "piatti": tavolo["ordini"].copy(),
        "totale": totale,
        "metodo": metodo_display,
        "data_ora": data_ora,
    })

    database.svuota_ordini_tavolo(tavolo["numero"])
    tavolo["ordini"].clear()
    print(f"Il Tavolo {tavolo['numero']} è ora libero. ✅")
        
"""Funzione per visualizzare lo storico degli ordini, mostrando il numero del tavolo, la data e l'ora dell'ordine, il metodo di pagamento e i piatti ordinati con i rispettivi prezzi. Se non ci sono ordini storici, stampa un messaggio informativo."""
def storico_ordini():
    if not storico_pagamenti:
        print("Nessun ordine storico disponibile.")
        return
    print("\n" + "-" * 40)
    print("Storico Ordini")
    print("-" * 40)
    for indice, ordine in enumerate(storico_pagamenti, start=1):
        print(f"\n{indice}. Tavolo {ordine['tavolo']} - {ordine['data_ora']} - {ordine['metodo']}")
        for piatto in ordine["piatti"]:
            print(f"  - {piatto['nome']} ({piatto['prezzo']}€)")
        print(f"  Totale: {ordine['totale']:.2f}€")

"""Funzione principale del programma, che mostra il menu principale e gestisce le scelte dell'utente, richiamando le funzioni appropriate per ciascuna opzione. Il ciclo continua fino a quando l'utente sceglie di uscire dal programma."""
def main():
    while True:
        mostra_menu()
        scelta = input("Scegli un'opzione: ")

        if scelta == "0":
            print("Uscita dal CRM del ristorante. ❌")
            break
        elif scelta == "1":
            gestione_menu()
        elif scelta == "2":
            gestione_tavoli()
        elif scelta == "3":
            nuovo_ordine()
        elif scelta == "4":
            pagamento()
        elif scelta == "5":
            storico_ordini()
        else:
            print("Scelta non valida. Riprova. 🚫")


if __name__ == "__main__":
    main()