
# tela_principal.py

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from modulos.abas.aba_cadastro import inicializar_cadastro
from modulos.abas.aba_clientes import montar_aba_clientes
from modulos.abas.aba_consulta import montar_aba_consulta
from modulos.abas.aba_financeiro import criar_aba_financeiro
from modulos.abas.aba_relatorios import criar_aba_relatorios
from modulos.componentes.mascote_widget import criar_aba_mascote_widget
from modulos.abas.aba_clima import montar_aba_clima
from modulos.recursos.aba_itau import criar_aba_itau
from modulos.abas.mensageiro import criar_aba_mensageiro
from modulos.abas.aba_config import montar_aba_config
from modulos.recursos.dados_compartilhados import montar_dados_compartilhados  # aqui montar_dados_compartilhados  grifado em vermelho
from modulos.abas.aba_som_legacy import criar_aba_som  # aqui criar_aba_som  grifado em vermelho
from modulos.abas.recursos import criar_aba_recursos
from recursos.som_expressao import som_e_expressao_acao
from recursos import dados_compartilhados as dc
from main import criar_player_som  # ou mova para player_som.py

from modulos.banco.database import testar_conexao
from recursos.conexao_utils import conexao_valida  # aqui conexao_valida  grifado em vermelho
from modulos.abas.menu_lateral import menu_lateral  # aqui criar_menu_lateral  grifado em vermelho
from modulos.componentes.barra_som_widget import criar_barra_som

from modulos.controladores.gerenciador_abas import GerenciadorAbas

gerenciador = GerenciadorAbas()

# registrar abas aqui...

menu = MenuLateral(frame_principal, perfil_usuario=usuario_logado.perfil, gerenciador_abas=gerenciador) # aqui MenuLateral frame_principal usuario_logado  grifado em vermelho
menu.grid(row=0, column=0, sticky="ns")


# Importações internas para evitar ciclos
gerenciador.registrar_aba("cadastro", lambda master: __import__("modulos.abas.aba_cadastro").abas.aba_cadastro.montar_aba_cadastro(master))
gerenciador.registrar_aba("financeiro", lambda master: __import__("modulos.abas.aba_financeiro").abas.aba_financeiro.montar_aba_financeiro(master))
gerenciador.registrar_aba("clientes", lambda master: __import__("modulos.abas.aba_clientes").abas.aba_clientes.montar_aba_clientes(master))
gerenciador.registrar_aba("editor_codigo", lambda master: __import__("modulos.abas.editor_codigo").abas.editor_codigo.AbaEditorCodigo(master))
gerenciador.registrar_aba("clima", lambda master: __import__("modulos.abas.aba_clima").abas.aba_clima.montar_aba_clima(master))
gerenciador.registrar_aba("config", lambda master: __import__("modulos.abas.aba_config").abas.aba_config.montar_aba_config(master))
gerenciador.registrar_aba("relatorios", lambda master: __import__("modulos.abas.aba_relatorios").abas.aba_relatorios.montar_aba_relatorios(master))
gerenciador.registrar_aba("itau", lambda master: __import__("modulos.abas.aba_itau").abas.aba_itau.montar_aba_itau(master))
gerenciador.registrar_aba("dados_compartilhados", lambda master: __import__("modulos.abas.aba_dados_compartilhados").abas.aba_dados_compartilhados.montar_aba_dados_compartilhados(master))
# ... e assim por diante

def verificar_conexao():
    testar_conexao()
    if conexao_valida():
        print("✅ Conexão OK")
    else:
        print("❌ Erro na conexão")

verificar_conexao()
####==============================================

def iniciar_janela_toplevel():
    frame_principal = tk.Frame(janela)
    frame_principal.grid(row=0, column=0, sticky="nsew")

    janela.grid_rowconfigure(0, weight=1)
    janela.grid_columnconfigure(0, weight=1)
    frame_principal.grid_rowconfigure(0, weight=1)
    frame_principal.grid_columnconfigure(1, weight=1)

    menu_lateral(frame_principal)

    conteudo = tk.Frame(frame_principal, bg="white")
    conteudo.grid(row=0, column=1, sticky="nsew")

    return janela

from modulos.componentes.menu_lateral_widget import MenuLateral

def iniciar_janela_principal(usuario_logado):
    root = tk.Tk()
    root.title("Sistema de Gestão")
    root.geometry("1200x700")
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    frame_principal = tk.Frame(root)
    frame_principal.grid(row=1, column=0, sticky="nsew")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    frame_principal.grid_rowconfigure(0, weight=1)
    frame_principal.grid_columnconfigure(0, weight=0)
    frame_principal.grid_columnconfigure(1, weight=0)
    frame_principal.grid_columnconfigure(2, weight=1)

    # posição no topo do player barra_som

    frame_topo = tk.Frame(root)
    frame_topo.grid(row=0, column=0, sticky="ew")
    frame_topo.grid_columnconfigure(0, weight=1)

    # Menu lateral comum
    menu = MenuLateral(frame_principal, perfil_usuario=usuario_logado.perfil)
    menu.grid(row=0, column=0, sticky="ns")

    # Menu auxiliar para administradores
    if usuario_logado.perfil == "admin":
        menu_admin = MenuAdmin(frame_principal)
        menu_admin.grid(row=0, column=1, sticky="ns")
        conteudo_coluna = 2
    else:
        conteudo_coluna = 1

    # Barra de som
    barra_som = criar_barra_som(frame_topo)
    barra_som.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

    # Área de conteúdo
    conteudo = tk.Frame(frame_principal, bg="white")
    conteudo.grid(row=0, column=conteudo_coluna, sticky="nsew")

    return root


class MenuLateral(tk.Frame):
    def __init__(self, master, perfil_usuario, gerenciador_abas):
        super().__init__(master, bg="#f0f0f0")
        self.gerenciador = gerenciador_abas
        self.perfil = perfil_usuario
        self.montar_menu()

    def montar_menu(self):
        abas_disponiveis = ["cadastro", "clientes", "editor_codigo", "clima", "config", "consulta", "financeiro", "relatórios", "itau", "dados_compartilhados"]

        if self.perfil == "admin":
            abas_disponiveis.append("editor_codigo")

        for i, nome_aba in enumerate(abas_disponiveis):
            btn = tk.Button(
                self,
                text=nome_aba.capitalize(),
                command=lambda aba=nome_aba: self.gerenciador.trocar_aba(aba, self.master)
            )
            btn.grid(row=i, column=0, sticky="ew", padx=10, pady=5)

        # Expande a coluna para ocupar toda a largura disponível
        self.grid_columnconfigure(0, weight=1)



















# def iniciar_janela_principal():
#     root = tk.Tk()
#     root.title("Sistema de Gestão")
#     root.geometry("1000x600")
#
#     frame_principal = tk.Frame(root)
#     frame_principal.grid(row=0, column=0, sticky="nsew")
#
#     root.grid_rowconfigure(0, weight=1)
#     root.grid_columnconfigure(0, weight=1)
#     frame_principal.grid_rowconfigure(0, weight=1)
#     frame_principal.grid_columnconfigure(1, weight=1)
#
#     menu = MenuLateral(frame_principal, perfil_usuario="admin")
#     menu.grid(row=0, column=0, sticky="ns")
#
#     conteudo = tk.Frame(frame_principal, bg="white")
#     conteudo.grid(row=0, column=1, sticky="nsew")
#
#     return root






# Janela principal

# def iniciar_janela_principal():
#     root = tk.Tk()
#     root.title("Sistema de Gestão")
#     root.geometry("1000x600")
#
#     frame_principal = tk.Frame(root)
#     frame_principal.grid(row=0, column=0, sticky="nsew")
#
#     root.grid_rowconfigure(0, weight=1)
#     root.grid_columnconfigure(0, weight=1)
#     frame_principal.grid_rowconfigure(0, weight=1)
#     frame_principal.grid_columnconfigure(1, weight=1)
#
#     menu_lateral(frame_principal)
#
#     conteudo = tk.Frame(frame_principal, bg="white")
#     conteudo.grid(row=0, column=1, sticky="nsew")
#
#     return root



# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Sistema de Gestão")
#     root.geometry("1000x600")  # Tamanho inicial da janela
#
#
#
# # Frame principal que contém o menu e o conteúdo
# frame_principal = tk.Frame(root)
# frame_principal.grid(row=0, column=0, sticky="nsew")
#
# # Configurações para redimensionamento
# root.grid_rowconfigure(0, weight=1)
# root.grid_columnconfigure(0, weight=1)
#
# frame_principal.grid_rowconfigure(0, weight=1)
# frame_principal.grid_columnconfigure(1, weight=1)  # coluna 1 será o conteúdo principal
#
# # Chamada da função que monta o menu lateral
# menu_lateral(frame_principal)
#
# # Frame de conteúdo (exemplo)
# conteudo = tk.Frame(frame_principal, bg="white")
# conteudo.grid(row=0, column=1, sticky="nsew")  # ao lado do menu
#
# # Inicia o loop da interface
# root.mainloop()






####==================================================


def caminho_imagem(nome):
    base = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base, "imagensipojucao", "imagens", nome)

def abrir_janela_principal(nome, perfil):
    janela = tk.Toplevel()
    janela.title(f"Ipojucão • Bem-vindo {nome}")
    janela.geometry("1024x768")

    dc.inicializar_variaveis(janela)

    notebook = ttk.Notebook(janela)
    notebook.pack(fill="both", expand=True)

    # Abas principais
    notebook.add(montar_aba_clientes(notebook), text="📋 Clientes")
    notebook.add(montar_aba_cadastro(notebook), text="📋 Cadastro")
    notebook.add(montar_aba_consulta(notebook), text="🔍 Consulta")
    notebook.add(criar_aba_financeiro(notebook), text="💰 Financeiro")
    notebook.add(criar_aba_relatorios(notebook), text="📊 Relatórios")
    notebook.add(montar_aba_clima(notebook), text="🌦️ Clima")
    notebook.add(criar_aba_itau(notebook), text="🏦 Itaú")
    notebook.add(criar_aba_mensageiro(notebook), text="📨 Mensageiro")
    notebook.add(criar_aba_mascote(notebook), text="🐾 Mascote")

    # Abas restritas
    if perfil == "admin":
        aba_config = ttk.Notebook(notebook)
        aba_config.add(criar_aba_som(aba_config), text="🔊 Som")
        aba_config.add(criar_aba_config(aba_config), text="🐶 Configurações PET")
        aba_config.add(montar_dados_compartilhados(aba_config), text="📦 Dados Compartilhados")
        aba_config.add(criar_aba_recursos(aba_config), text="📁 Recursos")
        notebook.add(aba_config, text="⚙️ Configurações")

    # Player de som
    player = criar_player_som(janela)
    player.pack(pady=10)

    janela.mainloop()



# # tela_principal.py
#
# import tkinter as tk
# from recursos.som_expressao import som_e_expressao_acao
# from PIL import Image, ImageTk
# import os
#
#
# import tkinter as tk
# from tkinter import ttk
#
#
# from modulos.banco.database import inicializar_banco
# from modulos.banco.database import Base, engine
#
#
# if __name__ == "__main__":
#     inicializar_banco()
#     iniciar_sistema()
#
#
# from modulos.abas.aba_clientes import montar_aba_clientes
# # outras abas...
#
#
#
# def criar_tela_principal(notebook):
#     frame = ttk.Frame(notebook)
#
#
#
# def criar_interface():
#     root = tk.Tk()
#     root.title("Sistema Principal")
#
#     notebook = ttk.Notebook(root)
#     notebook.pack(fill="both", expand=True)
#
#     aba_clientes = ttk.Frame(notebook)
#     notebook.add(aba_clientes, text="Clientes")
#     montar_aba_clientes(aba_clientes, inner_frame=None)
#
#     # outras abas...
#
#     root.mainloop()
#
# if __name__ == "__main__":
#     criar_interface()
#
# def caminho_imagem(nome):
#     base = os.path.dirname(os.path.dirname(__file__))
#     return os.path.join(base, "imagensipojucao", "imagens", nome)
#
# def abrir_janela_principal(nome, perfil):
#     janela = tk.Toplevel()
#     janela.title(f"Bem-vindo, {nome} ({perfil})")
#     janela.geometry("400x450")
#
#     # 🐶 Carrega imagem inicial do mascote
#     caminho_img_inicial = os.path.join(os.path.dirname(__file__), "imagens", "mascote_normal.png")
#     #imagem = Image.open(caminho_img_inicial).resize((150, 150))
#     imagem = Image.open(caminho_imagem("mascote_feliz.png")).resize((150, 150))
#     imagem_tk = ImageTk.PhotoImage(imagem)
#
#     print("Caminho mascote:", caminho_imagem("mascote_feliz.png"))
#     print("Existe?", os.path.exists(caminho_imagem("mascote_feliz.png")))
#
#     # 📌 Label que será atualizado com expressões
#     label_mascote = tk.Label(janela, image=imagem_tk)
#     label_mascote.image = imagem_tk
#     label_mascote.pack(pady=10)
#
#     # 👤 Informações do usuário
#     label_usuario = tk.Label(janela, text=f"Usuário: {nome}\nPerfil: {perfil}", font=("Arial", 12))
#     label_usuario.pack(pady=5)
#
#     # 🔘 Botões para testar reações
#     acoes = ["salvar", "editar", "excluir", "buscar"]
#     for acao in acoes:
#         botao = tk.Button(
#             janela,
#             text=acao.capitalize(),
#             width=20,
#             command=lambda ac=acao: som_e_expressao_acao(ac, label_mascote, janela)
#         )
#         botao.pack(pady=5)
#
#     janela.protocol("WM_DELETE_WINDOW", janela.destroy)
#
#
#
# def chamar_tela_principal(notebook):
#     frame = criar_tela_principal(notebook)
#     notebook.add(frame, text="Cadastro")
#
#
#
