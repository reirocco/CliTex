# CliTex - Minimal LaTeX Editor for Linux

CliTex è un'applicazione desktop moderna e minimalista scritta in Python, progettata per consentire agli utenti di scrivere, compilare e salvare documenti LaTeX in formato PDF in modo semplice e veloce.

## Caratteristiche principali

*   Interfaccia moderna e scura utilizzando CustomTkinter.
*   Area di testo dedicata per la scrittura del codice LaTeX.
*   Log di compilazione in tempo reale per monitorare errori e messaggi di pdflatex.
*   Esportazione rapida del PDF generato tramite pulsante dedicato.
*   Compilazione sicura tramite directory temporanee isolate.

## Prerequisiti

Per utilizzare questa applicazione, è necessario che il sistema abbia installato:

*   Python 3.x
*   Una distribuzione LaTeX (come TeX Live o MiKTeX) che includa il comando `pdflatex`.

## Installazione automatica (Linux)

Abbiamo incluso uno script di installazione (`install.sh`) per facilitare l'ambiente di lavoro:

1.  Assicurati che `install.sh` sia eseguibile:
    ```bash
    chmod +x install.sh
    ```
2.  Esegui l'installazione:
    ```bash
    ./install.sh
    ```

Questo script si occuperà di:
*   Creare un ambiente virtuale (`venv`).
*   Installare le dipendenze Python (`customtkinter`).
*   Configurare i percorsi corretti.
*   Creare una scorciatoia nel menu delle applicazioni del sistema.

## Utilizzo manuale

Se preferisci non utilizzare l'installer, puoi avviare l'applicazione manualmente seguendo questi passaggi:

1.  Crea un ambiente virtuale:
    ```bash
    python3 -m venv venv
    ```
2.  Installa le dipendenze:
    ```bash
    ./venv/bin/pip install -r requirements.txt
    ```
3.  Avvia l'app:
    ```bash
    ./venv/bin/python3 latex_app.py
    ```

## Requisiti di sistema esterni

L'applicazione comunica direttamente con `pdflatex`. Per installare i pacchetti necessari su diverse distribuzioni:

### Arch Linux
```bash
sudo pacman -S texlive-latex
```

### Debian / Ubuntu
```bash
sudo apt update && sudo apt install texlive-latex-base
```

## Struttura del progetto

*   latex_app.py: Il file sorgente principale in Python.
*   install.sh: Script di installazione automatica.
*   requirements.txt: Elenco delle librerie Python richieste.
*   README.md: Questa guida.

## Contributi

Contributi e segnalazioni di bug sono benvenuti. Si prega di aprire una Issue o una Pull Request per collaborare al miglioramento di LaTeXStudio.
