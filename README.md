# 🚀 CliTex - The Intelligent & Minimal LaTeX Workflow

**CliTex** transforms the chaotic LaTeX compilation process into a streamlined, high-performance experience. Built for developers, researchers, and 3D storytellers who need speed without the overhead of heavy IDEs.

> **Value Proposition:** Stop fighting with `pdflatex` logs. CliTex automates environmental cleaning, resolves missing dependencies (Smart-Fix), and provides a modern GUI for immediate PDF generation.

---

## ✨ Key Features

*   🎨 **Modern Dark UI:** Powered by CustomTkinter for a premium, distraction-free writing environment.
*   🧠 **Smart-Fix Engine:** Automatically detects and injects missing `listings` definitions (JS/TS) into temporary builds.
*   🧹 **Deep Clean:** Instantly removes non-ASCII artifacts (NBSP) and auto-corrects math-mode syntax.
*   📦 **One-Click DevOps:** Built-in system package installer for TeX Live extensions.
*   🔄 **OTA Updates:** Update your local installation directly from the GitHub main branch with one click.
*   📋 **Full Log View:** Dedicated tab for detailed stdout/stderr with clinical logging precision.

---

## 🛠️ Quick Installation (Linux)

Get up and running in seconds:

```bash
git clone https://github.com/reirocco/CliTex.git
cd CliTex
chmod +x install.sh
./install.sh
```

*Launch CliTex from your Application Menu or by typing `./clitex` in the terminal.*

---

## 🏗️ External System Requirements

CliTex communicates directly with your system's `pdflatex` engine. To install the necessary LaTeX collections:

### Arch Linux
```bash
sudo pacman -S texlive-latexextra texlive-langitalian texlive-fontsrecommended
```

### Debian / Ubuntu
```bash
sudo apt update && sudo apt install texlive-latex-extra texlive-lang-italian
```

---

## 📂 Project Structure

*   `latex_app.py`: The core intelligent Python engine.
*   `install.sh`: Automated Linux installer and desktop entry creator.
*   `clitex`: Local binary wrapper for quick terminal launch.
*   `clitex_icon.png`: Custom-made minimalist modern icon.
*   `.github/workflows/release.yml`: Automated CI/CD for standalone releases.
*   `update.sh`: Over-the-air update manager from GitHub.

---

## 🤝 Contributions

Contributi e segnalazioni di bug sono benvenuti. Si prega di aprire una Issue o una Pull Request per collaborare al miglioramento di CliTex.

---

## ⚖️ Disclaimer (Limitazione di Responsabilità)

Questo software è fornito "così com'è", senza garanzie di alcun tipo. In nessun caso lo sviluppatore sarà responsabile per reclami, danni (inclusa la perdita di dati o corruzione di file) o altre responsabilità derivanti dall'uso di CliTex o dall'integrazione con componenti di sistema come `pacman` e `pkexec`. L'uso di script con privilegi amministrativi è sotto l'esclusiva responsabilità dell'utente.

---
*Created with focus on productivity and design.*
