import tkinter as tk
from PIL import Image, ImageTk
import pygame

import os

from interface.aba_login_fusion import criar_login
from modulos.recursos.utils_imagem import carregar_imagem_projeto, carregar_arquivo_projeto

from modulos.recursos.dados_compartilhados import UsuarioLogado
from modulos.interface.tela_principal import iniciar_janela_principal



def tocar_som():
    caminho_som = carregar_arquivo_projeto("soft_edit_tune.mp3", subpasta="sons")
    print("Caminho som:", caminho_som)
    print("Existe?", os.path.exists(caminho_som))

    if os.path.exists(caminho_som):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(caminho_som)
            pygame.mixer.music.play()
        except Exception as e:
            print("Erro ao tocar som com pygame:", e)

        #threading.Thread(target=playsound, args=(caminho_som,), daemon=True).start()
def centralizar_janela(janela, largura, altura):
    x = (janela.winfo_screenwidth() - largura) // 2
    y = (janela.winfo_screenheight() - altura) // 2
    janela.geometry(f"{largura}x{altura}+{x}+{y}")


# def abrir_login():
#     splash.destroy()
#     from modulos.abas.aba_login_fusion import criar_login
#     criar_login()

# ABAIXO ALTERADO EM 31/01/2026
# def abrir_login_splash():
#
#     def montar_interface_login():
#         print("Login clicado")
#
#        #
#         tk.Label(janela_login, text="Usuário:").grid(row=0, column=0, padx=10, pady=10)
#         tk.Entry(janela_login).grid(row=0, column=1, padx=10, pady=10)
#
#         tk.Label(janela_login, text="Senha:").grid(row=1, column=0, padx=10, pady=10)
#         tk.Entry(janela_login, show="*").grid(row=1, column=1, padx=10, pady=10)
#
#         #tk.Button(janela_login, text="Entrar", command=lambda: print("Login clicado")).grid(row=2, columnspan=2, pady=20)
#         tk.Button(janela_login, text="Entrar", command=montar_interface_login).grid(row=2, columnspan=2, pady=20)
#
#     class UsuarioLogado:
#         def __init__(self, nome, perfil):
#             self.nome = nome
#             self.perfil = perfil
#
#     def ao_logar(nome, perfil):
#         class UsuarioLogado:
#             def __init__(self, nome, perfil):
#                 self.nome = nome
#                 self.perfil = perfil
#
#         usuario_logado = UsuarioLogado(nome, perfil)
#         janela_login.destroy()
#
#         from interface.tela_principal import iniciar_janela_principal
#         iniciar_janela_principal(usuario_logado)
#
#     #criar_login(ao_logar)
#     criar_login(janela_login, ao_logar_callback=ao_logar)
# ACIMA ALTERADO EM 31/01/2026


def abrir_login_splash():
    # Callback chamado após autenticação
    def ao_logar(nome, perfil):
        usuario_logado = UsuarioLogado(nome, perfil)
        # Fecha o splash e abre a tela principal
        # (o próprio criar_login deve destruir a janela ao logar, mas se não fizer, você pode chamar destroy aqui)
        iniciar_janela_principal(usuario_logado)



    # Chama criar_login passando a janela e o callback
    criar_login(ao_logar_callback=ao_logar)

    # ❌ Não criar Toplevel aqui
    # ✅ Apenas chamar criar_login passando o callback
    #criar_login(ao_logar)

    # def ao_logar(nome, perfil):
    #     janela_login.destroy()
    #     from interface.tela_principal import iniciar_janela_principal
    #     iniciar_janela_principal(usuario_logado=UsuarioTemporario())
    #
    # criar_login(janela_login, ao_logar_callback=ao_logar)
    # tk.Label(janela_login, text="Usuário:").grid(row=0, column=0)
    # tk.Entry(janela_login).grid(row=0, column=1)

def mostrar_splash():
    splash = tk.Tk()
    splash.title("Splash Screen")
    splash.configure(bg="white")
    splash.geometry("1300x800")
    splash.resizable(False, False)
    splash.attributes("-transparentcolor", "white")
    splash.configure(bg="white")
    # Centralizar na tela
    largura_tela = splash.winfo_screenwidth()
    altura_tela = splash.winfo_screenheight()
    x = (largura_tela // 2) - 1500
    y = (altura_tela // 2) - 150
    splash.geometry(f"1300x800+{x}+{y}")

    def iniciar_login_splash():
        splash.destroy()
        abrir_login_splash()

    splash.after(20000, iniciar_login_splash)  # ✅ agora a função já foi definida

    # Carregar logo
    try:
        caminho_logo = carregar_imagem_projeto("logo_ipojucao.png")
        img_logo = ImageTk.PhotoImage(Image.open(caminho_logo).resize((1800, 580)))
    except Exception as e:
        print("Erro ao carregar logo:", e)
        img_logo = None

    if img_logo:
        tk.Label(splash, image=img_logo, bg="white").place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(splash, text="Carregando...", fg="gray", bg="white", font=("Arial", 12)).place(relx=0.95, rely=0.95, anchor="se")

    # Tocar som após janela criada
    try:
        tocar_som()
    except Exception as e:
        print("Erro ao tocar som:", e)



    splash.mainloop()





splash = tk.Tk()
splash.overrideredirect(True)
splash.configure(bg="white")
splash.geometry("800x500")

largura_tela = splash.winfo_screenwidth()
altura_tela = splash.winfo_screenheight()
x = (largura_tela // 2) - 400
y = (altura_tela // 2) - 250
splash.geometry(f"800x500+{x}+{y}")

try:
    caminho_logo = carregar_imagem_projeto("logo_ipojucao.png")
    splash.img_logo = ImageTk.PhotoImage(Image.open(caminho_logo).resize((400, 120)), master=splash)

    caminho_mascote = carregar_imagem_projeto("mascote_coracao.png")
    splash.img_mascote = ImageTk.PhotoImage(Image.open(caminho_mascote).resize((100, 100)), master=splash)
except Exception as e:
    print("Erro ao carregar imagens:", e)
    splash.img_logo = splash.img_mascote = None

if splash.img_logo:
    tk.Label(splash, image=splash.img_logo, bg="white").place(relx=0.5, rely=0.4, anchor="center")

if splash.img_mascote:
    tk.Label(splash, image=splash.img_mascote, bg="white").place(relx=0.05, rely=0.85, anchor="sw")

tk.Label(splash, text="Carregando...", fg="gray", bg="white", font=("Arial", 12)).place(relx=0.95, rely=0.95, anchor="se")

tocar_som()
splash.after(5000, abrir_login_splash)
splash.mainloop()














# import tkinter as tk
# from PIL import Image, ImageTk
# from playsound import playsound
# import threading
# import os
# from modulos.recursos.utils_imagem import carregar_imagem_projeto, carregar_arquivo_projeto
#
# # Função para tocar som em paralelo
# def tocar_som():
#     caminho_som = carregar_arquivo_projeto("clair_de_lune_prelude.mp3", subpasta="sons")
#     if os.path.exists(caminho_som):
#         threading.Thread(target=playsound, args=(caminho_som,), daemon=True).start()
#
# # Janela principal
# splash = tk.Tk()
# splash.title("Splash Screen")
# splash.configure(bg="white")  # fundo branco ou neutro
# splash.geometry("800x500")    # janela maior e centralizada
# splash.resizable(False, False)
#
# # Centralizar na tela
# largura_tela = splash.winfo_screenwidth()
# altura_tela = splash.winfo_screenheight()
# x = (largura_tela // 2) - 400
# y = (altura_tela // 2) - 250
# splash.geometry(f"800x500+{x}+{y}")
#
# # Carregar logo
# try:
#     caminho_logo = carregar_imagem_projeto("logo_ipojucao.png")
#     img_logo = ImageTk.PhotoImage(Image.open(caminho_logo).resize((400, 120)))
# except Exception as e:
#     print("Erro ao carregar logo:", e)
#     img_logo = None
#
# # Exibir logo centralizado
# if img_logo:
#     label_logo = tk.Label(splash, image=img_logo, bg="white")
#     label_logo.place(relx=0.5, rely=0.4, anchor="center")
#
# # Texto "Carregando..." no canto inferior direito
# label_texto = tk.Label(splash, text="Carregando...", fg="gray", bg="white", font=("Arial", 12))
# label_texto.place(relx=0.95, rely=0.95, anchor="se")
#
# # Iniciar som
# tocar_som()
#
# # Exibir janela
# splash.mainloop()
#






















# import tkinter as tk
# from PIL import Image, ImageTk
# from playsound import playsound
# import threading
# import os
#
# #from utils_imagem import carregar_imagem_projeto
# from modulos.recursos.utils_imagem import carregar_imagem_projeto
#
# try:
#     caminho = carregar_imagem_projeto("logo_ipojucao.png")
#     print("Caminho:", caminho)
#     print("Existe?", os.path.exists(caminho))
#
#     img_pil = Image.open(caminho)
#     img_redimensionada = img_pil.resize((400, 120))
#     img_logo = ImageTk.PhotoImage(img_redimensionada)
#     print("Imagem carregada com sucesso!")
#
# except Exception as e:
#     print("Erro:", e)
#
#
#
# # Função para carregar imagem com caminho relativo
# import os
#
#
#
# # def carregar_imagem_projeto(nome_arquivo):
# #     caminho_base = r"C:\Users\VEIRANO\PycharmProjects\ModuloTkinter\PlanilhaControleIpojucão\imagensipojucao"
# #     caminho_completo = os.path.join(caminho_base, nome_arquivo)
# #     return caminho_completo
#
# # def carregar_imagem_projeto(nome_arquivo):
# #     caminho_base = r"C:\Users\VEIRANO\PycharmProjects\ModuloTkinter\Planilha Controle Ipojucão\imagensipojucao"
# #     caminho_completo = os.path.join(caminho_base, nome_arquivo)
# #     return caminho_completo
#
# # Função para tocar som em paralelo
# def tocar_som():
#     from modulos.recursos.utils_imagem import carregar_arquivo_projeto
#
#     caminho_som = carregar_arquivo_projeto("clair_de_lune_prelude.mp3", subpasta="sons")
#     print("Caminho som:", caminho_som)
#     print("Existe?", os.path.exists(caminho_som))
#
#     if os.path.exists(caminho_som):
#         threading.Thread(target=playsound, args=(caminho_som,), daemon=True).start()
#     else:
#         print("Som não encontrado:", caminho_som)
#
# # Alternância entre mascotes
# def alternar_mascote():
#     atual = label_img.cget("image")
#     novo = img_beijo if atual == str(img_coracao) else img_coracao
#     label_img.configure(image=novo)
#     splash.after(1000, alternar_mascote)
#
# # Janela principal
# splash = tk.Tk()
# splash.title("Splash Screen")
# splash.configure(bg="black")
# splash.geometry("600x400")
# splash.resizable(False, False)
#
# # Layout centralizado
# splash.grid_rowconfigure(0, weight=1)
# splash.grid_columnconfigure(0, weight=1)
#
# frame = tk.Frame(splash, bg="black")
# frame.grid(row=0, column=0, sticky="nsew")
# frame.grid_columnconfigure(0, weight=1)
#
# # Carregar imagens
# caminho = carregar_imagem_projeto("logo_ipojucao.png")
# print("Caminho testado:", caminho)
# print("Existe?", os.path.exists(caminho))
#
# img_pil = Image.open(caminho)
# img_redimensionada = img_pil.resize((400, 120))
# img_logo = ImageTk.PhotoImage(img_redimensionada)
# img_logo1 = ImageTk.PhotoImage(Image.open(carregar_imagem_projeto("logo_ipojucao.png")).resize((400, 120)))
# img_coracao = ImageTk.PhotoImage(Image.open(carregar_imagem_projeto("mascote_coracao.png")).resize((150, 150)))
# img_beijo = ImageTk.PhotoImage(Image.open(carregar_imagem_projeto("mascote_beijo.png")).resize((150, 150)))
#
# # Widgets
# label_logo = tk.Label(frame, image=img_logo, bg="black")
# label_logo.grid(row=0, column=0, pady=(30, 10), sticky="n")
#
# label_img = tk.Label(frame, image=img_coracao, bg="black")
# label_img.grid(row=1, column=0, pady=(10, 10), sticky="n")
#
# label_texto = tk.Label(frame, text="Carregando...", fg="white", bg="black", font=("Arial", 14))
# label_texto.grid(row=2, column=0, sticky="n")
#
# # Iniciar som e animação
# tocar_som()
# alternar_mascote()
#
# # Exibir janela
# splash.mainloop()