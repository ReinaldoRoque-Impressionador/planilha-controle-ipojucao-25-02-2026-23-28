import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

class AbaEditorCodigo(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.caminho_arquivo = None
        self._criar_widgets()

    def _criar_widgets(self):
        # Botões de controle
        frame_botoes = tk.Frame(self)
        frame_botoes.grid(row=0, column=0, sticky="ew", padx=10, pady=5)


        btn_abrir = tk.Button(frame_botoes, text="Abrir Arquivo", command=self._abrir_arquivo)
        btn_abrir.grid(row=0, column=0, padx=5)


        btn_salvar = tk.Button(frame_botoes, text="Salvar", command=self._salvar_arquivo)
        btn_salvar.grid(row=0, column=1, padx=5)


        # Editor de texto com rolagem
        self.editor = ScrolledText(self, wrap="none", font=("Courier New", 12))
        self.editor.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)


    def _abrir_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Abrir arquivo Python",
            filetypes=[("Arquivos Python", "*.py"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    conteudo = f.read()
                self.editor.delete("1.0", tk.END)
                self.editor.insert(tk.END, conteudo)
                self.caminho_arquivo = caminho
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir o arquivo:\n{e}")

    def _salvar_arquivo(self):
        if not self.caminho_arquivo:
            caminho = filedialog.asksaveasfilename(
                title="Salvar como",
                defaultextension=".py",
                filetypes=[("Arquivos Python", "*.py"), ("Todos os arquivos", "*.*")]
            )
            if not caminho:
                return
            self.caminho_arquivo = caminho

        try:
            conteudo = self.editor.get("1.0", tk.END)
            with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(conteudo)
            messagebox.showinfo("Sucesso", "Arquivo salvo com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o arquivo:\n{e}")