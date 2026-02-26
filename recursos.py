import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from recursos.utilitarios import listar_arquivos, caminho_arquivo
from recursos.som import tocar_som

def criar_aba_recursos(notebook):
    frame = ttk.Frame(notebook)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="📁 Visualizador de Recursos", font=("Arial", 14)).pack(pady=10)

    # 🎨 Combobox de imagens
    ttk.Label(frame, text="Imagens disponíveis:").pack()
    imagens = listar_arquivos("imagens", [".png", ".jpg"])
    imagem_var = tk.StringVar()
    imagem_combo = ttk.Combobox(frame, textvariable=imagem_var, values=imagens, state="readonly", width=30)
    imagem_combo.pack(pady=5)

    # 🖼️ Label para exibir imagem
    label_imagem = ttk.Label(frame)
    label_imagem.pack(pady=10)

    def mostrar_imagem():
        nome = imagem_var.get()
        caminho = caminho_arquivo(nome)
        try:
            img = Image.open(caminho).resize((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            label_imagem.config(image=img_tk)
            label_imagem.image = img_tk
        except Exception as e:
            print(f"[ERRO] Falha ao carregar imagem: {e}")

    ttk.Button(frame, text="🖼️ Mostrar Imagem", command=mostrar_imagem).pack(pady=5)

    # 🎵 Combobox de sons
    ttk.Label(frame, text="Sons disponíveis:").pack()
    sons = listar_arquivos("som", [".mp3", ".wav"])
    som_var = tk.StringVar()
    som_combo = ttk.Combobox(frame, textvariable=som_var, values=sons, state="readonly", width=30)
    som_combo.pack(pady=5)

    def tocar_som_selecionado():
        nome = som_var.get()
        caminho = caminho_arquivo(nome, "som")
        tocar_som(caminho)

    ttk.Button(frame, text="▶️ Tocar Som", command=tocar_som_selecionado).pack(pady=5)

    return frame