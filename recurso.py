import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from recursos import tocar_som
import os

def criar_aba_recursos(notebook):
    frame = ttk.Frame(notebook)
    frame.grid(row=0, column=0, sticky="nsew")

    ttk.Label(frame, text="📁 Visualizador de Recursos")


    # 🎵 Combobox de sons
    ttk.Label(frame, text="Sons disponíveis:").grid(row=4, column=0, sticky="w")
    sons = listar_arquivos("som", [".mp3", ".wav"])
    som_var = tk.StringVar()
    som_combo = ttk.Combobox(frame, textvariable=som_var, values=sons, state="readonly", width=30)
    som_combo.grid(row=4, column=1, pady=5, sticky="ew")

    def tocar_som_selecionado():
        nome = som_var.get()
        caminho = caminho_arquivo(nome, "som")
        tocar_som(caminho)

    ttk.Button(frame, text="▶️ Tocar Som", command=tocar_som_selecionado).grid(row=5, column=0, columnspan=2, pady=5)

    return frame


def caminho_arquivo(nome_arquivo, subpasta="imagens"):
    pasta_base = os.path.dirname(__file__)
    caminho = os.path.join(pasta_base, "..", subpasta, nome_arquivo)
    return os.path.abspath(caminho)

def listar_arquivos(pasta, extensoes):
    caminho_base = os.path.join(os.path.dirname(__file__), "..", pasta)
    caminho_base = os.path.abspath(caminho_base)

    arquivos = []
    for nome in os.listdir(caminho_base):
        if any(nome.lower().endswith(ext) for ext in extensoes):
            arquivos.append(nome)
    return arquivos

    # 🎨 Combobox de imagens
    ttk.Label(frame, text="Imagens disponíveis:").grid(row=0, column=0, sticky="w", padx=10, pady=5)

    imagens = listar_arquivos("imagens", [".png", ".jpg"])
    imagem_var = tk.StringVar()
    imagem_combo = ttk.Combobox(frame, textvariable=imagem_var, values=imagens, state="readonly", width=30)
    imagem_combo.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    # 🖼️ Label para exibir imagem
    label_imagem = ttk.Label(frame)
    label_imagem.grid(row=1, column=0, columnspan=2, pady=10)

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

    ttk.Button(frame, text="🖼️ Mostrar Imagem", command=mostrar_imagem).grid(row=2, column=0, columnspan=2, pady=5)    # 🎵 Combobox de sons
    ttk.Label(frame, text="Sons disponíveis:").grid(row=6, column=0, sticky="w", padx=10, pady=5)

    sons = listar_arquivos("som", [".mp3", ".wav"])
    som_var = tk.StringVar()
    som_combo = ttk.Combobox(frame, textvariable=som_var, values=sons, state="readonly", width=30)
    som_combo.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

    def tocar_som_selecionado():
        nome = som_var.get()
        caminho = caminho_arquivo(nome, "som")
        tocar_som(caminho)

    ttk.Button(frame, text="▶️ Tocar Som", command=tocar_som_selecionado).grid(row=7, column=0, columnspan=2, pady=10)








    # # 🎨 Combobox de imagens
    # ttk.Label(frame, text="Imagens disponíveis:").grid(row=1, column=0, sticky="w")
    # imagens = listar_arquivos("imagens", [".png", ".jpg"])
    # imagem_var = tk.StringVar()
    # imagem_combo = ttk.Combobox(frame, textvariable=imagem_var, values=imagens, state="readonly", width=30)
    # imagem_combo.grid(row=1, column=1, pady=5, sticky="ew")
    #
    # # 🖼️ Label para exibir imagem
    # label_imagem = ttk.Label(frame)
    # label_imagem.grid(row=2, column=0, columnspan=2, pady=10)
    #
    # def mostrar_imagem():
    #     nome = imagem_var.get()
    #     caminho = caminho_arquivo(nome)
    #     try:
    #         img = Image.open(caminho).resize((150, 150))
    #         img_tk = ImageTk.PhotoImage(img)
    #         label_imagem.config(image=img_tk)
    #         label_imagem.image = img_tk
    #     except Exception as e:
    #         print(f"[ERRO] Falha ao carregar imagem: {e}")
    #
    # ttk.Button(frame, text="🖼️ Mostrar Imagem", command=mostrar_imagem).grid(row=3, column=0, columnspan=2, pady=5)
