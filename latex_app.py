import os
import subprocess
import tempfile
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

# Configurazione del tema
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class LaTeXApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LatexStudio - Modern LaTeX Editor")
        self.geometry("1100x750")

        # Configurazione layout (2 colonne)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar / Editor Section (Left) ---
        self.editor_frame = ctk.CTkFrame(self)
        self.editor_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.editor_frame.grid_rowconfigure(1, weight=1)
        self.editor_frame.grid_columnconfigure(0, weight=1)

        self.editor_label = ctk.CTkLabel(self.editor_frame, text="LaTeX Code", font=ctk.CTkFont(size=14, weight="bold"))
        self.editor_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.text_editor = ctk.CTkTextbox(self.editor_frame, font=("Courier New", 13))
        self.text_editor.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        # Default LaTeX content
        self.text_editor.insert("0.0", self.get_default_template())

        # Bottoni Editor
        self.editor_toolbar = ctk.CTkFrame(self.editor_frame, fg_color="transparent")
        self.editor_toolbar.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        self.compile_btn = ctk.CTkButton(self.editor_toolbar, text="Compile PDF", command=self.compile_latex, corner_radius=8)
        self.compile_btn.pack(side="left", padx=5)

        self.export_btn = ctk.CTkButton(self.editor_toolbar, text="Save PDF As...", command=self.save_pdf, corner_radius=8, state="disabled")
        self.export_btn.pack(side="left", padx=5)

        self.update_btn = ctk.CTkButton(self.editor_toolbar, text="Check Updates", command=self.check_updates, corner_radius=8, fg_color="#333333", hover_color="#444444")
        self.update_btn.pack(side="right", padx=5)

        # --- Status / Preview Section (Right) ---
        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.status_frame.grid_rowconfigure(1, weight=1)
        self.status_frame.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(self.status_frame, text="Compilation Status & Logs", font=ctk.CTkFont(size=14, weight="bold"))
        self.status_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.log_viewer = ctk.CTkTextbox(self.status_frame, state="disabled", font=("Courier New", 12), fg_color="#1a1a1a")
        self.log_viewer.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        # Variabili di stato
        self.temp_dir: str = ""
        self.last_pdf_path: str = ""

    def get_default_template(self):
        return r"""\documentclass{article}
\usepackage[utf8]{inputenc}

\title{Mio Documento LaTeX}
\author{Autore}
\date{\today}

\begin{document}
\maketitle

\section{Introduzione}
Scrivi qui il tuo codice LaTeX.
Puoi usare formule come $E=mc^2$.

\section{Lista}
\begin{itemize}
    \item Primo elemento
    \item Secondo elemento
\end{itemize}

\end{document}
"""

    def log(self, message):
        self.log_viewer.configure(state="normal")
        self.log_viewer.insert("end", message + "\n")
        self.log_viewer.see("end")
        self.log_viewer.configure(state="disabled")

    def clear_logs(self):
        self.log_viewer.configure(state="normal")
        self.log_viewer.delete("0.0", "end")
        self.log_viewer.configure(state="disabled")

    def compile_latex(self):
        code = self.text_editor.get("0.0", "end").strip()
        if not code:
            messagebox.showwarning("Attenzione", "Il codice LaTeX è vuoto.")
            return

        self.clear_logs()
        self.log("Avvio compilazione...")
        self.compile_btn.configure(state="disabled")

        # Creazione directory temporanea stabile per questa sessione
        if not self.temp_dir:
            self.temp_dir = tempfile.mkdtemp(prefix="latexapp_")

        tex_file_path = os.path.join(self.temp_dir, "document.tex")
        
        try:
            with open(tex_file_path, "w", encoding="utf-8") as f:
                f.write(code)
            
            # Esecuzione pdflatex
            # Usiamo -interaction=nonstopmode per evitare blocchi
            args = ["pdflatex", "-interaction=nonstopmode", "-output-directory", self.temp_dir, tex_file_path]
            process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()
            
            self.log(stdout)
            if stderr:
                self.log("ERRORS:\n" + stderr)

            if process.returncode == 0:
                self.log("\nSuccesso! PDF generato correttamente.")
                self.last_pdf_path = os.path.join(self.temp_dir, "document.pdf")
                self.export_btn.configure(state="normal")
                messagebox.showinfo("Successo", "Compilazione completata con successo!")
            else:
                self.log(f"\nErrore durante la compilazione (Return Code: {process.returncode})")
                messagebox.showerror("Errore", "La compilazione ha fallito. Controlla i log.")
                self.export_btn.configure(state="disabled")

        except FileNotFoundError:
            self.log("ERRORE: 'pdflatex' non trovato nel sistema. Assicurati che TeX Live o MiKTeX siano installati.")
            messagebox.showerror("Errore di Sistema", "Comando 'pdflatex' non trovato.")
        except Exception as e:
            self.log(f"ERRORE IMPREVISTO: {str(e)}")
            messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")
        
        self.compile_btn.configure(state="normal")

    def save_pdf(self):
        if not self.last_pdf_path or not os.path.exists(self.last_pdf_path):
            messagebox.showwarning("Attenzione", "Nessun PDF disponibile per il salvataggio.")
            return

        target_file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Salva il PDF"
        )
        
        if target_file:
            try:
                shutil.copy(self.last_pdf_path, target_file)
                messagebox.showinfo("Salvato", f"File salvato con successo in:\n{target_file}")
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile salvare il file: {str(e)}")

    def check_updates(self):
        # Esegui lo script update.sh
        script_path = os.path.join(os.getcwd(), "update.sh")
        if not os.path.exists(script_path):
            messagebox.showerror("Errore", "Script di aggiornamento (update.sh) non trovato.")
            return

        self.log("\nControllo aggiornamenti in corso...")
        try:
            # Eseguiamo in un terminale separato o semplicemente catturiamo l'output
            process = subprocess.Popen(
                ["/bin/bash", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()
            
            if "fatal: .git non è un repository Git" in stderr or "fatal: not a git repository" in stderr:
                self.log("ERRORE: La cartella non è un repository Git. Inizializzala prima con 'git init'.")
                messagebox.showwarning("Aggiornamento", "Repository Git non trovato. Leggi i log per istruzioni.")
            elif process.returncode == 0:
                self.log(stdout)
                messagebox.showinfo("Aggiornamento", "App aggiornata con successo! Riavvia l'applicazione per applicare le modifiche.")
            else:
                self.log(stderr)
                messagebox.showerror("Errore", "L'aggiornamento ha fallito. Controlla la connessione o i conflitti Git.")
        except Exception as e:
            self.log(f"Errore durante l'esecuzione dell'aggiornamento: {str(e)}")

    def __del__(self):
        # Pulizia cartella temporanea alla chiusura
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except:
                pass

if __name__ == "__main__":
    app = LaTeXApp()
    app.mainloop()
