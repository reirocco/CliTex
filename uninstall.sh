#!/bin/bash

# Abort on error / show steps
set -e

APP_NAME="CliTex"
INSTALL_DIR=$(pwd)
VENV_DIR="$INSTALL_DIR/venv"
DESKTOP_FILE="$HOME/.local/share/applications/clitex.desktop"
BINARY_NAME="clitex"

echo "=== Inizio Disinstallazione di $APP_NAME ==="

# 1. Rimuovere file .desktop dal menu applicazioni
if [ -f "$DESKTOP_FILE" ]; then
    echo "Rimozione della scorciatoia nel menu applicazioni..."
    rm "$DESKTOP_FILE"
fi

# 2. Rimuovere ambiente virtuale
if [ -d "$VENV_DIR" ]; then
    echo "Rimozione dell'ambiente virtuale (venv)..."
    rm -rf "$VENV_DIR"
fi

# 3. Rimuovere il binary wrappet (clitex)
if [ -f "$INSTALL_DIR/$BINARY_NAME" ]; then
    echo "Rimozione dello script di avvio '$BINARY_NAME'..."
    rm "$INSTALL_DIR/$BINARY_NAME"
fi

# 4. Pulire cache Python
echo "Pulizia file temporanei e __pycache__..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# 5. Rimuovere link di sistema se presente
if [ -f "/usr/local/bin/$BINARY_NAME" ]; then
    echo "INFO: Per rimuovere anche il link simbolico di sistema, esegui: sudo rm /usr/local/bin/$BINARY_NAME"
fi

echo "=== Disinstallazione Completata! ==="
echo "Nota: I file sorgente (.py, .md, .sh) e l'icona in questa cartella non sono stati toccati."
echo "Puoi cancellare la cartella '$INSTALL_DIR' se vuoi rimuovere tutto."
