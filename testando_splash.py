import tkinter as tk
from PIL import Image, ImageTk
from playsound import playsound
import threading
import os
from modulos.recursos.utils_imagem import carregar_arquivo_projeto
from modulos.recursos.utils_imagem import carregar_imagem_projeto


# # Função para carregar imagem com caminho relativo
# def carregar_imagem_projeto(nome_arquivo, subpasta="imagens"):
#     caminho_base = os.path.dirname(__file__)
#     return os.path.join(caminho_base, subpasta, nome_arquivo)

# Função para tocar som em paralelo
def tocar_som():
    caminho_som = carregar_arquivo_projeto("clair_de_lune_prelude.mp3", subpasta="sons")
    if os.path.exists(caminho_som):
        threading.Thread(target=playsound, args=(caminho_som,), daemon=True).start()
    else:
        print("Som não encontrado:", caminho_som)

# Alternância entre mascotes
def alternar_mascote():
    atual = label_img.cget("image")
    novo = img_beijo if atual == str(img_coracao) else img_coracao
    label_img.configure(image=novo)
    splash.after(1000, alternar_mascote)

# Janela principal
splash = tk.Tk()
splash.title("Splash Screen")
splash.configure(bg="black")
splash.geometry("600x400")
splash.resizable(False, False)

# Layout centralizado
splash.grid_rowconfigure(0, weight=1)
splash.grid_columnconfigure(0, weight=1)

frame = tk.Frame(splash, bg="black")
frame.grid(row=0, column=0, sticky="nsew")
frame.grid_columnconfigure(0, weight=1)

# Carregar imagens
img_logo = ImageTk.PhotoImage(Image.open(carregar_imagem_projeto("logo_ipojucao.png")).resize((400, 120)))
print(carregar_imagem_projeto("logo_ipojucao.png"))
img_coracao = ImageTk.PhotoImage(Image.open(carregar_imagem_projeto("mascote_coracao.png")).resize((150, 150)))
img_beijo = ImageTk.PhotoImage(Image.open(carregar_imagem_projeto("mascote_beijo.png")).resize((150, 150)))

# Widgets
label_logo = tk.Label(frame, image=img_logo, bg="black")
label_logo.grid(row=0, column=0, pady=(30, 10), sticky="n")

label_img = tk.Label(frame, image=img_coracao, bg="black")
label_img.grid(row=1, column=0, pady=(10, 10), sticky="n")

label_texto = tk.Label(frame, text="Carregando...", fg="white", bg="black", font=("Arial", 14))
label_texto.grid(row=2, column=0, sticky="n")

# Iniciar som e animação
tocar_som()
alternar_mascote()

# Exibir janela
splash.mainloop()
#
