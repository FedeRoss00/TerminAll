"""
Main file per il programma CRM. Consente all'utente di scegliere tra diverse categorie di CRM preimpostate.
"""
import ristorante_crm
import negozio_crm
import sport_crm

def categorie():
    """Definisco le categorie di CRM disponibili e le stampo a video."""
    print("\n" + "=" * 20)
    print("Scegli una delle categorie di CRM già preimpostate:")
    print("=" * 20)
    print("0. Esci ❌")
    print("1. Ristorante 🍽️")
    print("2. Negozio 🏪")
    print("3. Consulenza Sportiva 🏋️‍♂️")
    print("=" * 20)

def main():
    """Gestisco il flusso principale del programma, consentendo all'utente di scegliere una categoria di CRM o uscire."""
    while True:
        categorie()
        scelta = input("Scegli un'opzione: ")

        if scelta == "0":
            print("Uscita dal programma.")
            break
        elif scelta == "1":
            ristorante_crm.main()
        elif scelta == "2":
            negozio_crm.main()
        elif scelta == "3":
            sport_crm.main()
        else:
            print("Scelta non valida. Riprova. 🚫")

if __name__ == "__main__":
    main()
    