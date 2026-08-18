from datetime import datetime
import database_sport as database

database.inizializza_database()

clienti = database.carica_clienti()
peso_fisico = database.carica_peso_fisico()
massa_magra = database.carica_massa_magra()
massa_grassa = database.carica_massa_grassa()
contratti = database.carica_contratti()


def mostra_menu():
    print("\n" + "=" * 40)
    print("Menu Consulenza Sportiva")
    print("=" * 40)
    print("0. Esci ❌")
    print("1. Aggiungi cliente 🧍‍♂️")
    print("2. Visualizza clienti 📋")
    print("3. Aggiungi misurazione fisica ⚖️")
    print("4. Visualizza misurazioni fisiche 📊")
    print("5. Aggiungi contratto 📄")
    print("6. Visualizza contratti 📑")
    print("=" * 40)


