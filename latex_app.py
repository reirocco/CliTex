import os
import subprocess
import tempfile
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import re

# Configurazione del tema
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Definizioni librerie "Smart-Fix" per linguaggi listings mancanti
SMART_FIXES = {
    "javascript": r"""
\lstdefinelanguage{JavaScript}{
  keywords={break, case, catch, continue, debugger, default, delete, do, else, false, finally, for, function, if, in, instanceof, new, null, return, switch, this, throw, true, try, typeof, var, void, while, with, let, const},
  morecomment=[l]{//},
  morecomment=[s]{/*}{*/},
  morestring=[b]',
  morestring=[b]",
  ndkeywords={class, export, boolean, throw, implements, import, this},
  keywordstyle=\color{blue}\bfseries,
  ndkeywordstyle=\color{darkgray}\bfseries,
  identifierstyle=\color{black},
  commentstyle=\color{purple}\ttfamily,
  stringstyle=\color{red}\ttfamily,
  sensitive=true
}
""",
    "typescript": r"""
\lstdefinelanguage{TypeScript}{
  keywords={abstract, any, as, boolean, break, case, catch, class, console, const, continue, debugger, declare, default, delete, do, else, enum, export, extends, false, finally, for, function, get, if, implements, import, in, instanceof, interface, let, module, namespace, never, new, null, number, object, package, private, protected, public, readonly, require, return, set, static, string, super, switch, symbol, this, throw, true, try, typeof, type, var, void, while, with, yield},
  morecomment=[l]{//},
  morecomment=[s]{/*}{*/},
  morestring=[b]',
  morestring=[b]",
  keywordstyle=\color{blue}\bfseries,
  ndkeywordstyle=\color{darkgray}\bfseries,
  identifierstyle=\color{black},
  commentstyle=\color{purple}\ttfamily,
  stringstyle=\color{red}\ttfamily,
  sensitive=true
}
"""
}

class CliTexApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CliTex - Intelligent & Clean LaTeX Editor")
        self.geometry("1100x850")

        # Configurazione layout tab
        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.tab_editor = self.tabview.add("Editor")
        self.tab_logs = self.tabview.add("Full Logs")

        # --- Tab Editor ---
        self.tab_editor.grid_columnconfigure(0, weight=3)
        self.tab_editor.grid_columnconfigure(1, weight=1)
        self.tab_editor.grid_rowconfigure(0, weight=1)

        # Editor Frame
        self.editor_frame = ctk.CTkFrame(self.tab_editor, fg_color="transparent")
        self.editor_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.editor_frame.grid_rowconfigure(1, weight=1)
        self.editor_frame.grid_columnconfigure(0, weight=1)

        self.editor_label = ctk.CTkLabel(self.editor_frame, text="LaTeX Code", font=ctk.CTkFont(size=14, weight="bold"))
        self.editor_label.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="w")

        self.text_editor = ctk.CTkTextbox(self.editor_frame, font=("Courier New", 14), corner_radius=10)
        self.text_editor.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.text_editor.insert("0.0", self.get_default_template())

        # Bindings
        self.text_editor.bind("<Control-a>", self.select_all_text)
        self.text_editor.bind("<Control-A>", self.select_all_text)

        # Status Frame
        self.status_frame = ctk.CTkFrame(self.tab_editor, fg_color="#2b2b2b", corner_radius=10)
        self.status_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.summary_label = ctk.CTkLabel(self.status_frame, text="Status", font=ctk.CTkFont(size=14, weight="bold"))
        self.summary_label.pack(pady=(15, 5))

        self.status_indicator = ctk.CTkLabel(self.status_frame, text="READY", font=ctk.CTkFont(size=16), text_color="#3498db")
        self.status_indicator.pack(pady=10)

        self.last_msg_label = ctk.CTkLabel(self.status_frame, text="Pronto.", wraplength=200, font=ctk.CTkFont(size=12))
        self.last_msg_label.pack(pady=20, padx=10)

        # Toolbar Bottom
        self.toolbar = ctk.CTkFrame(self.tab_editor, fg_color="transparent")
        self.toolbar.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        self.compile_btn = ctk.CTkButton(self.toolbar, text="Compile PDF", command=self.compile_latex, corner_radius=8, width=150)
        self.compile_btn.pack(side="left", padx=5)

        self.clean_btn = ctk.CTkButton(self.toolbar, text="Clean & Format", command=self.perform_full_clean, corner_radius=8, fg_color="#16a085", hover_color="#1abc9c")
        self.clean_btn.pack(side="left", padx=5)

        self.save_btn = ctk.CTkButton(self.toolbar, text="Save PDF", command=self.save_pdf, corner_radius=8, width=120, state="disabled")
        self.save_btn.pack(side="left", padx=5)

        self.update_btn = ctk.CTkButton(self.toolbar, text="Update", command=self.check_updates, corner_radius=8, fg_color="#333333", hover_color="#444444", width=100)
        self.update_btn.pack(side="right", padx=5)

        self.extras_btn = ctk.CTkButton(self.toolbar, text="TeX Tools", command=self.install_latex_extras, corner_radius=8, fg_color="#2c3e50", width=120)
        self.extras_btn.pack(side="right", padx=5)

        # --- Tab Logs ---
        self.log_toolbar = ctk.CTkFrame(self.tab_logs, fg_color="transparent")
        self.log_toolbar.pack(fill="x", padx=10, pady=(10, 0))
        self.copy_log_btn = ctk.CTkButton(self.log_toolbar, text="Copia Log negli Appunti", command=self.copy_logs, corner_radius=8, fg_color="#34495e")
        self.copy_log_btn.pack(side="left")

        self.log_viewer = ctk.CTkTextbox(self.tab_logs, font=("Courier New", 12), fg_color="#1a1a1a")
        self.log_viewer.pack(fill="both", expand=True, padx=10, pady=10)
        self.log_viewer.configure(state="disabled")

        # State
        self.temp_dir: str = ""
        self.last_pdf_path: str = ""

    def get_default_template(self):
        return r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[italian]{babel}
\usepackage{xcolor}
\usepackage{listings}

\title{CliTex Intelligent Editor}
\begin{document}
\maketitle

\section{Introduzione}
Scrivi qui il tuo codice. CliTex pulirà caratteri invisibili e sistemerà la matematica.

\begin{itemize}
\item Esempio di math: $E=mc^2$
\item Simbolo maggiore senza math: > (CliTex lo correggerà)
\end{itemize}

\end{document}
"""

    def log(self, message, is_summary=False):
        self.log_viewer.configure(state="normal")
        self.log_viewer.insert("end", message + "\n")
        self.log_viewer.see("end")
        self.log_viewer.configure(state="disabled")
        if is_summary:
            self.last_msg_label.configure(text=message)

    def select_all_text(self, event=None):
        self.text_editor.tag_add("sel", "1.0", "end")
        self.text_editor.mark_set("insert", "1.0")
        self.text_editor.see("insert")
        return "break"

    def copy_logs(self):
        self.clipboard_clear()
        self.clipboard_append(self.log_viewer.get("0.0", "end"))
        messagebox.showinfo("Copia", "Log copiati!")

    def set_status(self, status, color="#3498db"):
        self.status_indicator.configure(text=status.upper(), text_color=color)

    def clean_latex(self, code):
        """Pulisce caratteri non-ASCII e corregge sintassi comune."""
        # 1. Rimuovi spazi non-breaking e altri invisibili
        code = code.replace("\xa0", " ") # NBSP
        code = code.replace("\u200b", "") # zero-width space
        
        # 2. Correzione Itemize/Enumerate (indentazione minima)
        code = re.sub(r'\\item\s*', r'  \\item ', code)
        
        # 3. Correzione simboli matematici isolati nel testo
        # Cerchiamo > o < che non sono preceduti o seguiti da $ o [ ]
        # Nota: questa regex è semplificata
        code = re.sub(r'(?<![\$\[])([><])(?![\$\]])', r'$\1$', code)
        
        return code

    def perform_full_clean(self):
        code = self.text_editor.get("0.0", "end")
        cleaned_code = self.clean_latex(code)
        self.text_editor.delete("0.0", "end")
        self.text_editor.insert("0.0", cleaned_code)
        self.log("Pulizia e formattazione completata.", True)

    def compile_latex(self, retry_with_fix=None):
        code = self.text_editor.get("0.0", "end").strip()
        if not code: return

        # Pulizia automatica leggera prima di compilare
        if not retry_with_fix:
            code = self.clean_latex(code)
            self.log("--- Nuova Compilazione (Auto-Cleaned) ---", True)

        code_to_compile = retry_with_fix if retry_with_fix else code

        self.set_status("COMPILING" if not retry_with_fix else "RE-COMPILING", "#f1c40f")
        self.compile_btn.configure(state="disabled")

        if not self.temp_dir:
            self.temp_dir = tempfile.mkdtemp(prefix="clitex_")

        tex_path = os.path.join(self.temp_dir, "document.tex")
        
        try:
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(code_to_compile)
            
            args = ["pdflatex", "-interaction=nonstopmode", "-output-directory", self.temp_dir, tex_path]
            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            
            self.log(stdout)
            if stderr: self.log(stderr)

            if process.returncode == 0:
                self.set_status("SUCCESS", "#2ecc71")
                self.log("PDF generato.", True)
                self.last_pdf_path = os.path.join(self.temp_dir, "document.pdf")
                self.save_btn.configure(state="normal")
            else:
                # AUTO-FIX Listings
                match = re.search(r"language\s+([a-zA-Z0-9]+)\s+undefined", stdout + stderr, re.IGNORECASE)
                if match and not retry_with_fix:
                    lang = match.group(1).lower()
                    if lang in SMART_FIXES:
                        self.log(f"Auto-Fix: Iniezione linguaggio '{lang}'...", True)
                        fixed_code = self.apply_smart_fix(code, lang)
                        self.compile_latex(retry_with_fix=fixed_code)
                        return

                self.set_status("ERROR", "#e74c3c")
                if "not set up for use with LaTeX" in stdout + stderr:
                    self.log("Errore Unicode: usa 'Clean & Format' per rimuovere caratteri invisibili.", True)
                else:
                    self.log("Compilazione fallita.", True)
                self.save_btn.configure(state="disabled")

        except Exception as e:
            self.set_status("SYSTEM ERROR", "#e74c3c")
            self.log(f"Errore Sistema: {str(e)}", True)
        
        self.compile_btn.configure(state="normal")

    def apply_smart_fix(self, current_code, lang):
        fix_content = SMART_FIXES[lang]
        if "\\begin{document}" in current_code:
            # NOTA LE DOPPIE GRAFFE {{document}} QUI SOTTO:
            return current_code.replace("\\begin{document}", f"{fix_content}\n\\begin{{document}}")
        return fix_content + "\n" + current_code

    def save_pdf(self):
        if not self.last_pdf_path: return
        target = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if target:
            shutil.copy(self.last_pdf_path, target)
            self.log(f"PDF salvato.", True)

    def check_updates(self):
        self.set_status("UPDATING...", "#9b59b6")
        script = os.path.join(os.getcwd(), "update.sh")
        try:
            process = subprocess.Popen(["/bin/bash", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                self.set_status("UPDATED", "#2ecc71")
                self.log("Riavvia l'app.", True)
            else:
                self.set_status("FAIL", "#e74c3c")
        except: pass

    def install_latex_extras(self):
        if not messagebox.askyesno("Install", "Installare extras TeX?"): return
        self.set_status("INSTALLING...", "#e67e22")
        cmd = ["pkexec", "pacman", "-S", "--noconfirm", "texlive-latexextra", "texlive-langitalian", "texlive-fontsrecommended"]
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                self.set_status("INSTALLED", "#2ecc71")
                self.log("Pronto!", True)
        except: pass

    def __del__(self):
        if self.temp_dir and os.path.exists(self.temp_dir):
            try: shutil.rmtree(self.temp_dir)
            except: pass

if __name__ == "__main__":
    app = CliTexApp()
    app.mainloop()
