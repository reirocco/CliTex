#!/bin/bash

# Abort on error
set -e

APP_NAME="LaTeXStudio"
INSTALL_DIR=$(pwd)
VENV_DIR="$INSTALL_DIR/venv"
PYTHON_BIN="/usr/bin/python3"
DESKTOP_FILE="$HOME/.local/share/applications/latexstudio.desktop"

echo "=== Inizio Installazione di $APP_NAME ==="

# 1. Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "Errore: Python3 non trovato. Per favore installalo."
    exit 1
fi

# 2. Creazione Ambiente Virtuale
echo "Creazione dell'ambiente virtuale in $VENV_DIR..."
python3 -m venv "$VENV_DIR"

# 3. Installazione dipendenze Python
echo "Installazione dipendenze da requirements.txt..."
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r "$INSTALL_DIR/requirements.txt"

# 4. Verifica pdflatex (LaTeX)
echo "Verifica di pdflatex..."
if ! command -v pdflatex &> /dev/null; then
    echo "ATTENZIONE: 'pdflatex' non è stato trovato nel sistema."
    echo "L'applicazione richiede LaTeX per funzionare correttamente."
    echo "Su sistemi basati su Arch Linux, installalo con: sudo pacman -S texlive-latex"
    echo "Su sistemi basati su Debian/Ubuntu: sudo apt install texlive-latex-base"
else
    echo "pdflatex trovato!"
fi

# 5. Creazione script di avvio (Wrapper)
echo "Creazione dello script di avvio..."
cat <<EOF > "$INSTALL_DIR/run_app.sh"
#!/bin/bash
cd "$INSTALL_DIR"
./venv/bin/python3 latex_app.py
EOF
chmod +x "$INSTALL_DIR/run_app.sh"

# 6. Creazione file .desktop per il menu applicazioni
echo "Creazione scorciatoia nel menu applicazioni..."
cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Type=Application
Name=LaTeXStudio
Comment=Editor LaTeX Moderno
Exec=$INSTALL_DIR/run_app.sh
Path=$INSTALL_DIR
Terminal=false
Categories=Office;Development;
EOF

chmod +x "$DESKTOP_FILE"

echo "=== Installazione Completata! ==="
echo "Puoi avviare l'app dal tuo menu applicazioni o eseguendo ./run_app.sh"
