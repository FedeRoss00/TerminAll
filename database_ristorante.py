"""
database_ristorante.py - livello di persistenza del CRM ristorante.

Solo funzioni di salvataggio/caricamento su SQLite: nessuna logica di
interfaccia qui dentro. Copre piatti, tavoli, ordini in corso e
storico dei pagamenti.

Nota su PRAGMA foreign_keys = ON: in SQLite, a differenza di altri
database, i vincoli di chiave esterna NON sono attivi di default -
vanno abilitati esplicitamente ad ogni connessione, altrimenti
verrebbero semplicemente ignorati.
"""

import sqlite3

NOME_DATABASE = "crm_ristorante.db"


def ottieni_connessione():
    connessione = sqlite3.connect(NOME_DATABASE)
    connessione.execute("PRAGMA foreign_keys = ON")
    return connessione


def inizializza_database():
    connessione = ottieni_connessione()
    cursore = connessione.cursor()

    cursore.execute("""
        CREATE TABLE IF NOT EXISTS piatti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            prezzo REAL NOT NULL
        )
    """)

    cursore.execute("""
        CREATE TABLE IF NOT EXISTS tavoli (
            numero INTEGER PRIMARY KEY
        )
    """)

    cursore.execute("""
        CREATE TABLE IF NOT EXISTS ordini_correnti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tavolo_numero INTEGER NOT NULL,
            piatto_nome TEXT NOT NULL,
            piatto_prezzo REAL NOT NULL,
            FOREIGN KEY (tavolo_numero) REFERENCES tavoli (numero)
        )
    """)

    cursore.execute("""
        CREATE TABLE IF NOT EXISTS storico_pagamenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tavolo_numero INTEGER NOT NULL,
            totale REAL NOT NULL,
            metodo TEXT NOT NULL,
            data_ora TEXT NOT NULL
        )
    """)

    cursore.execute("""
        CREATE TABLE IF NOT EXISTS storico_piatti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            storico_id INTEGER NOT NULL,
            piatto_nome TEXT NOT NULL,
            piatto_prezzo REAL NOT NULL,
            FOREIGN KEY (storico_id) REFERENCES storico_pagamenti (id)
        )
    """)

    connessione.commit()
    connessione.close()


# --- Piatti (menu) ---

def carica_piatti():
    connessione = ottieni_connessione()
    cursore = connessione.cursor()
    cursore.execute("SELECT id, nome, prezzo FROM piatti")
    righe = cursore.fetchall()
    connessione.close()
    return [{"id": r[0], "nome": r[1], "prezzo": r[2]} for r in righe]


def salva_piatto(nome, prezzo):
    connessione = ottieni_connessione()
    cursore = connessione.cursor()
    cursore.execute("INSERT INTO piatti (nome, prezzo) VALUES (?, ?)", (nome, prezzo))
    connessione.commit()
    nuovo_id = cursore.lastrowid
    connessione.close()
    return nuovo_id


def elimina_piatto(id_piatto):
    connessione = ottieni_connessione()
    cursore = connessione.cursor()
    cursore.execute("DELETE FROM piatti WHERE id = ?", (id_piatto,))
    connessione.commit()
    connessione.close()


# --- Tavoli e ordini in corso ---

def salva_numero_tavoli(numero):
    """Sostituisce i tavoli esistenti con 'numero' tavoli nuovi e vuoti.
    Cancella anche gli ordini in corso, perche' stiamo reimpostando
    il ristorante da capo."""
    connessione = ottieni_connessione()
    cursore = connessione.cursor()
    cursore.execute("DELETE FROM ordini_correnti")
    cursore.execute("DELETE FROM tavoli")
    for i in range(1, numero + 1):
        cursore.execute("INSERT INTO tavoli (numero) VALUES (?)", (i,))
    connessione.commit()
    connessione.close()


def carica_tavoli():
    """Ricostruisce la lista dei tavoli, ognuno con i propri ordini in corso."""
    connessione = ottieni_connessione()
    cursore = connessione.cursor()
    cursore.execute("SELECT numero FROM tavoli ORDER BY numero")
    numeri_tavoli = [riga[0] for riga in cursore.fetchall()]

    tavoli = []
    for numero in numeri_tavoli:
        cursore.execute(
            "SELECT id, piatto_nome, piatto_prezzo FROM ordini_correnti WHERE tavolo_numero = ?",
            (numero,),
        )
        ordini = [
            {"id_ordine": r[0], "nome": r[1], "prezzo": r[2]}
            for r in cursore.fetchall()
        ]
        tavoli.append({"numero": numero, "ordini": ordini})

    connessione.close()
    return tavoli


def salva_ordine_tavolo(tavolo_numero, nome, prezzo):
    """Registra un piatto ordinato su un tavolo, restituendo l'id della riga."""
    connessione = ottieni_connessione()
    cursore = connessione.cursor()
    cursore.execute(
        "INSERT INTO ordini_correnti (tavolo_numero, piatto_nome, piatto_prezzo) VALUES (?, ?, ?)",
        (tavolo_numero, nome, prezzo),
    )
    connessione.commit()
    nuovo_id = cursore.lastrowid
    connessione.close()
    return nuovo_id


def elimina_ordine_tavolo(id_ordine):
    connessione = ottieni_connessione()
    cursore = connessione.cursor()
    cursore.execute("DELETE FROM ordini_correnti WHERE id = ?", (id_ordine,))
    connessione.commit()
    connessione.close()


def svuota_ordini_tavolo(tavolo_numero):
    """Cancella tutti gli ordini in corso di un tavolo (usato dopo il pagamento)."""
    connessione = ottieni_connessione()
    cursore = connessione.cursor()
    cursore.execute("DELETE FROM ordini_correnti WHERE tavolo_numero = ?", (tavolo_numero,))
    connessione.commit()
    connessione.close()


# --- Storico pagamenti ---

def salva_pagamento(tavolo_numero, piatti, totale, metodo, data_ora):
    """Salva un pagamento nello storico, con il dettaglio dei piatti."""
    connessione = ottieni_connessione()
    cursore = connessione.cursor()
    cursore.execute(
        "INSERT INTO storico_pagamenti (tavolo_numero, totale, metodo, data_ora) VALUES (?, ?, ?, ?)",
        (tavolo_numero, totale, metodo, data_ora),
    )
    storico_id = cursore.lastrowid

    for piatto in piatti:
        cursore.execute(
            "INSERT INTO storico_piatti (storico_id, piatto_nome, piatto_prezzo) VALUES (?, ?, ?)",
            (storico_id, piatto["nome"], piatto["prezzo"]),
        )

    connessione.commit()
    connessione.close()


def carica_storico():
    """Ricostruisce lo storico dei pagamenti, ognuno col proprio dettaglio piatti."""
    connessione = ottieni_connessione()
    cursore = connessione.cursor()
    cursore.execute(
        "SELECT id, tavolo_numero, totale, metodo, data_ora FROM storico_pagamenti ORDER BY id"
    )
    righe_storico = cursore.fetchall()

    storico = []
    for storico_id, tavolo_numero, totale, metodo, data_ora in righe_storico:
        cursore.execute(
            "SELECT piatto_nome, piatto_prezzo FROM storico_piatti WHERE storico_id = ?",
            (storico_id,),
        )
        piatti = [{"nome": r[0], "prezzo": r[1]} for r in cursore.fetchall()]
        storico.append({
            "tavolo": tavolo_numero,
            "piatti": piatti,
            "totale": totale,
            "metodo": metodo,
            "data_ora": data_ora,
        })

    connessione.close()
    return storico