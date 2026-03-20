#!/bin/bash

# Abort on error
set -e

APP_NAME="CliTex"
BINARY_NAME="clitex"
INSTALL_DIR=$(pwd)
VENV_DIR="$INSTALL_DIR/venv"
DESKTOP_FILE="$HOME/.local/share/applications/clitex.desktop"
ICON_PATH="$INSTALL_DIR/clitex_icon.png"

echo "=== Inizio Installazione di $APP_NAME ==="

# 1. Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "Errore: Python3 non trovato. Per favore installalo."
    exit 1
fi

# 2. Creazione Ambiente Virtuale
echo "Creazione dell'ambiente virtuale..."
python3 -m venv "$VENV_DIR"

# 3. Installazione dipendenze Python
echo "Installazione dipendenze..."
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r "$INSTALL_DIR/requirements.txt"

# 4. Creazione script di avvio locale
echo "Creazione dello script di avvio: $BINARY_NAME"
cat <<EOF > "$INSTALL_DIR/$BINARY_NAME"
#!/bin/bash
cd "$INSTALL_DIR"
./venv/bin/python3 latex_app.py "\$@"
EOF
chmod +x "$INSTALL_DIR/$BINARY_NAME"

# 5. Creazione file .desktop per il menu applicazioni
echo "Configurazione icona e scorciatoia menu..."
cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Type=Application
Name=$APP_NAME
Comment=Minimal LaTeX Editor
Exec=$INSTALL_DIR/$BINARY_NAME
Icon=$ICON_PATH
Path=$INSTALL_DIR
Terminal=false
Categories=Office;Development;
EOF

chmod +x "$DESKTOP_FILE"

echo "=== Installazione Completata! ==="
echo "Ora puoi:"
echo "1. Cercare 'CliTex' nel tuo menu applicazioni."
echo "2. Avviare l'app da terminale in questa cartella con: ./$BINARY_NAME"
echo ""
echo "TIP: Per avviare 'clitex' da ovunque nel terminale, aggiungi questa cartella al tuo PATH o crea un link simbolico:"
echo "sudo ln -sf $INSTALL_DIR/$BINARY_NAME /usr/local/bin/$BINARY_NAME"
