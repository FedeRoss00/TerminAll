# CRM Multi-Settore da Terminale

Un CRM leggero e portabile, scritto in Python, pensato per essere eseguito da terminale su qualsiasi sistema operativo (Windows, macOS, Linux). L'idea di fondo è avere un'unica base di codice adattabile a diversi tipi di attività — ristoranti, negozi, aziende di qualsiasi settore — sviluppando via via i moduli specifici per ciascun ambito a partire da un nucleo comune.

## Obiettivi del progetto

- **Leggerezza** — nessuna dipendenza pesante, ci si affida il più possibile alla libreria standard di Python
- **Portabilità** — la stessa base di codice funziona identica su Windows, macOS e Linux
- **Installazione semplice** — al momento basta avere Python installato; in futuro sarà disponibile anche un file di installazione/eseguibile che non richiederà nemmeno quello
- **Modularità** — ogni tipo di attività è pensato come un modulo a sé stante, così il progetto può crescere aggiungendo nuovi settori senza dover riscrivere le fondamenta

## Requisiti

- Python 3.8 o superiore
- Nessuna libreria esterna richiesta (solo libreria standard), salvo diversa indicazione futura

## Come si esegue

Ogni modulo del CRM è uno script Python autonomo, eseguibile con:

```bash
python nome_modulo.py
```

Su Windows, se il comando `python` non è riconosciuto, usa `py nome_modulo.py`.

## Roadmap

- [ ] Persistenza dei dati (salvataggio su file o database)
- [ ] Espansione a più settori di attività
- [ ] Architettura client-server per l'utilizzo da più dispositivi contemporaneamente
- [ ] File di installazione/eseguibile standalone per ogni sistema operativo