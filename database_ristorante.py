"""
database.py - livello di persistenza del CRM.

Questo modulo si occupa SOLO di salvare e caricare dati da SQLite.
Non contiene print() né input(): il suo compito e' fare da "ponte"
tra il programma e il file del database, cosi' il resto del codice
non ha bisogno di sapere COME i dati vengono salvati, solo che puo'
chiedere a queste funzioni di farlo.

sqlite3 e' un modulo della libreria standard di Python: non serve
installare nessun server ne' nessuna libreria esterna. Il database
e' semplicemente un file sul disco (crm_ristorante.db), creato in
automatico alla prima esecuzione.
"""

import sqlite3

NOME_DATABASE = "crm_ristorante.db"


def ottieni_connessione():
    """Apre (creandolo se non esiste) il file del database."""
    return sqlite3.connect(NOME_DATABASE)


def inizializza_database():
    """Crea le tabelle se non esistono ancora. Va chiamata all'avvio del programma."""
    connessione = ottieni_connessione()
    cursore = connessione.cursor()

    cursore.execute("""
        CREATE TABLE IF NOT EXISTS piatti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            prezzo REAL NOT NULL
        )
    """)

    connessione.commit()
    connessione.close()


def carica_piatti():
    """Legge tutti i piatti salvati e li restituisce come lista di dizionari,
    nello stesso formato che il programma gia' usa in memoria."""
    connessione = ottieni_connessione()
    cursore = connessione.cursor()
    cursore.execute("SELECT id, nome, prezzo FROM piatti")
    righe = cursore.fetchall()
    connessione.close()

    piatti = []
    for id_piatto, nome, prezzo in righe:
        piatti.append({"id": id_piatto, "nome": nome, "prezzo": prezzo})
    return piatti


def salva_piatto(nome, prezzo):
    """Inserisce un nuovo piatto nel database e restituisce l'id assegnato."""
    connessione = ottieni_connessione()
    cursore = connessione.cursor()
    cursore.execute("INSERT INTO piatti (nome, prezzo) VALUES (?, ?)", (nome, prezzo))
    connessione.commit()
    nuovo_id = cursore.lastrowid
    connessione.close()
    return nuovo_id


def elimina_piatto(id_piatto):
    """Rimuove un piatto dal database dato il suo id."""
    connessione = ottieni_connessione()
    cursore = connessione.cursor()
    cursore.execute("DELETE FROM piatti WHERE id = ?", (id_piatto,))
    connessione.commit()
    connessione.close()