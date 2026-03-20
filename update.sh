#!/bin/bash

# Abort on error
set -e

INSTALL_DIR=$(pwd)
VENV_DIR="$INSTALL_DIR/venv"

echo "=== Verifica Aggiornamenti ==="

# 1. Verifica se è un repository Git
if [ ! -d ".git" ]; then
    echo "Errore: Questa cartella non è inizializzata come repository Git."
    echo "Esegui prima: git init && git remote add origin ISTRUZIONI_REPO"
    exit 1
fi

# 2. Pull dei cambiamenti
echo "Recupero degli ultimi commit da GitHub..."
if git pull origin main; then
    echo "Repository aggiornato con successo."
else
    echo "Errore durante il git pull. Controlla la connessione o eventuali conflitti."
    exit 1
fi

# 3. Aggiornamento dipendenze
if [ -f "requirements.txt" ]; then
    echo "Aggiornamento dipendenze Python..."
    "$VENV_DIR/bin/pip" install -r requirements.txt
fi

echo "=== Aggiornamento Completato! ==="
echo "Ora puoi riavviare l'applicazione."
