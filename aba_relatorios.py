# aba_relatorios.py
#📦 Estrutura principal do arquivo


import tkinter as tk
from PIL import Image,ImageTk
from tkinter import ttk
from tkcalendar import DateEntry
import os
import pygame

# Sons e imagens
# Banco e modelos
#from modulos.banco.db_models import Pagamento
from modulos.banco.database import Cliente, Tutor, Usuario, Pagamento, Pets
from modulos.banco.database import database
from modulos.recursos import dados_compartilhados as dc

from modulos.recursos.som import tocar_som, tocar_som_curto, parar_som, alternar_som, continuar_som
from modulos.abas.mensageiro import enviar_mensagem_whatsapp
from modulos.recursos.funcoes_auxiliares import caminho_arquivo



from modulos.banco.database import testar_conexao
from modulos.recursos.conexao_utils import conexao_valida

from modulos.recursos import dados_compartilhados as dc
from sqlalchemy import Date, Time
from sqlalchemy import DateTime
from datetime import datetime






import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os
import pygame
from collections import defaultdict
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
agora = datetime.now()

from estrutura import inner_frame



# Banco e recursos
from modulos.banco.database import Cliente, Tutor, Usuario, Pagamento, Pets, database
from modulos.recursos import dados_compartilhados as dc
from modulos.abas.mensageiro import enviar_mensagem_whatsapp
from modulos.recursos.funcoes_auxiliares import caminho_arquivo
from modulos.recursos.som import alternar_som
from modulos.recursos.centro_controle_relatorios import gerar_relatorio_pdf, gerar_excel
import pywhatkit as kit
from modulos.recursos.utils_mensagens import enviar_mensagem_whatsapp
from modulos.banco.database import Atendimento, Pagamento
from modulos.recursos.utils_mensagens import salvar_relatorio_pdf
from modulos.banco.database import Cliente, Pets


# === Variáveis globais ===
checkbox_vars = {}
calendario_inicial = None
calendario_final = None
campo_relatorio = None
combobox_categorias = None
combobox_subcategoria = None




# === Dados dos comboboxes ===
combobox_data = {
    "Serviços": [
        "Banho", "Hidratação", "Desembolo", "Remoção Pelos",
        "Corte Unhas", "Escovação Dentes", "Tosa Higiênica",
        "Tosa Máquina", "Tosa Tesoura", "Leva Trás"
    ],
    "Cadastro": [
        "Cadastrado Desde", "Nome Pet", "Idade", "Tutor 1", "Tutor 2",
        "Telefone Tutor 1", "Email Tutor 1", "Telefone Tutor 2",
        "Email Tutor 2", "Endereço", "Número", "Complemento", "Recomendações"
    ],
    "Pagamentos": [
        "Condições Pagamento", "Abatimentos", "Status Pagamento",
        "Data Pagamento", "Forma Pagamento"
    ],
    "Financeiro": [
        "Valores em Aberto", "Valores Recebidos",
        "Recebidos via PIX", "Recebidos por Cartão de Crédito"
    ],
    "Comparativos": [
        "Banhos PETs Pequenos", "Banhos PETs Médios",
        "Tosas PETs Grandes"
    ]
}


def montar_aba_relatorios(inner_frame):
    frame = ttk.Frame(inner_frame)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # --- Área superior ---
    top_frame = ttk.Frame(frame)
    top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    ttk.Label(top_frame, text="Relatórios", font=("Segoe UI", 14, "bold")).grid(
        row=0, column=0, columnspan=len(combobox_data)+2, pady=10, sticky="w"
    )

    # Comboboxes múltiplos (Serviços, Cadastro, Pagamentos, Financeiro, Comparativos)
    comboboxes = criar_comboboxes(top_frame, combobox_data)

    # Campos de data
    criar_calendarios(top_frame)

    # Área inferior (campo de relatório com scroll)
    criar_frame_relatorio(frame)

    # Frame de administradores
    criar_frame_admins(frame)

    # Botões principais
    criar_botoes(frame)

    # Relatórios financeiros
    criar_frame_financeiro(frame)



    return frame


# # === Funções auxiliares ===
# def criar_comboboxes(frame, data_dict):
#     comboboxes = {}
#     col = 0
#     for i in range(len(data_dict)):
#         frame.grid_columnconfigure(i, weight=1)
#     for categoria, valores in data_dict.items():
#         cb = ttk.Combobox(frame, values=valores)
#         cb.grid(row=1, column=col, padx=5, pady=5, sticky="ew")
#         cb.set(categoria)
#         comboboxes[categoria] = cb
#         col += 1
#
#     global combobox_categorias
#     combobox_categorias = ttk.Combobox(frame,
#                                        values=["Financeiro", "Serviços", "Cadastro", "Pagamentos", "Comparativos"],
#                                        state="readonly")
#     combobox_categorias.set("Financeiro")
#     combobox_categorias.grid(row=0, column=0, padx=5, pady=5)
#
#     global combobox_categorias, combobox_subcategoria
#     combobox_categorias = ttk.Combobox(frame,
#                                        values=["Financeiro", "Serviços", "Cadastro", "Pagamentos", "Comparativos"],
#                                        state="readonly")
#     combobox_categorias.set("Financeiro")
#     combobox_categorias.grid(row=0, column=0, padx=5, pady=5)
#
#     combobox_subcategoria = ttk.Combobox(frame, state="readonly")
#     combobox_subcategoria.grid(row=0, column=1, padx=5, pady=5)
#
#     ttk.Label(frame, text="Categoria:").grid(row=0, column=0, padx=5, pady=5)
#     combobox_categorias = ttk.Combobox(frame,
#                                        values=["Financeiro", "Serviços", "Cadastro", "Pagamentos", "Comparativos"],
#                                        state="readonly")
#     combobox_categorias.grid(row=1, column=0, padx=5, pady=5)
#
#     return comboboxes

def criar_comboboxes(frame, data_dict):
    comboboxes = {}
    col = 0

    # Configura colunas
    for i in range(len(data_dict)):
        frame.grid_columnconfigure(i, weight=1)

    # Cria comboboxes individuais com título acima
    for categoria, valores in data_dict.items():
        # Título acima do combobox
        ttk.Label(frame, text=categoria).grid(row=1, column=col, padx=5, pady=5)

        # Combobox com valores da categoria
        cb = ttk.Combobox(frame, values=valores, state="readonly")
        cb.grid(row=2, column=col, padx=5, pady=5, sticky="ew")
        cb.set("Selecione")  # texto inicial

        comboboxes[categoria] = cb
        col += 1

    return comboboxes

def criar_calendarios(inner_frame):
    global calendario_inicial, calendario_final
    frame_datas = ttk.LabelFrame(inner_frame, text="Período do Relatório")
    frame_datas.grid(
        sticky="ew", padx=10, pady=5)
    ttk.Label(frame_datas, text="Data Inicial:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    calendario_inicial = DateEntry(frame_datas, locale="pt_BR", width=12)
    calendario_inicial.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    ttk.Label(frame_datas, text="Data Final:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    calendario_final = DateEntry(frame_datas, locale="pt_BR", width=12)
    calendario_final.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

def criar_frame_relatorio(container):
    global campo_relatorio, frame_relatorio

    frame_relatorio = ttk.Frame(container)
    frame_relatorio.grid(row=3, column=0, sticky="nsew")
    campo_relatorio = tk.Text(frame_relatorio, wrap="none", borderwidth=2, relief="solid")
    campo_relatorio.grid(row=0, column=0, sticky="nsew")
    scroll_y = ttk.Scrollbar(frame_relatorio, orient="vertical", command=campo_relatorio.yview)
    scroll_y.grid(row=0, column=1, sticky="ns")
    campo_relatorio.configure(yscrollcommand=scroll_y.set)

# admin_lista = [
#     {"nome": "Reinaldo", "telefone": "5511981772847"},
#     {"nome": "Raphael", "telefone": "5511981078611"},
#     {"nome": "Lindinalva", "telefone": "5511963174904"}
# ]

admin_lista = [
    {"nome": "RAPHAEL", "telefone": "+5511989078611"},
    {"nome": "LINDINALVA", "telefone": "+5511963174904"},
    {"nome": "MARLENE", "telefone": "+5511963405229"},
    {"nome": "REINALDO", "telefone": "+5511981772847"}
]

def criar_frame_admins(container):
    frame_admins = ttk.LabelFrame(container, text="Administradores para notificação")
    frame_admins.grid(row=3, column=1, padx=10, pady=10)
    for i, admin in enumerate(admin_lista):
        var = tk.BooleanVar()
        checkbox_vars[admin["telefone"]] = var
        tk.Checkbutton(frame_admins, text=admin["nome"], variable=var).grid(row=i, column=0, sticky="w")

def notificar_admins():
    mensagem = campo_relatorio.get('1.0', 'end').strip()
    print("Mensagem a enviar:", mensagem)
    for telefone, var in checkbox_vars.items():
        if var.get():
            numero = f"+{telefone}"  # adiciona o + aqui
            enviar_mensagem_whatsapp(f"+{telefone}", mensagem)
            print("Enviando para:", numero)
            enviar_mensagem_whatsapp(numero, mensagem)


def criar_botoes(container):
    botoes_frame = ttk.Frame(container)
    botoes_frame.grid(row=5, column=0, pady=10)
    ttk.Button(botoes_frame, text="Gerar Relatório", command=gerar_relatorio).grid(row=0, column=0, padx=5)
    ttk.Button(botoes_frame, text="Limpar Relatório", command=limpar_relatorio).grid(row=0, column=1, padx=5)
    ttk.Button(botoes_frame, text="Notificar Admins", command=notificar_admins).grid(row=0, column=2, padx=5)
    ttk.Button(botoes_frame, text="📤 Exportar Planilha", command=dc.exportar_para_planilha).grid(row=0, column=3, padx=5)
    return botoes_frame

def limpar_relatorio():
    campo_relatorio.delete('1.0', 'end')


def gerar_relatorio_servicos(data_i, data_f):
    atendimentos = database.query(Atendimento).filter(
        Atendimento.data_hora_servico >= data_i,
        Atendimento.data_hora_servico <= data_f
    ).all()

    resumo = defaultdict(lambda: {"quantidade": 0})

    for a in atendimentos:
        # Divide os serviços realizados em lista
        servicos = a.servicos_realizados.split(",") if a.servicos_realizados else []
        for servico in servicos:
            servico = servico.strip()
            if servico:
                resumo[servico]["quantidade"] += 1

    texto = f"🐾 Relatório de Serviços\n🗓️ De: {data_i} até {data_f}\n\n"
    if not resumo:
        texto += "Nenhum serviço encontrado neste período."
    else:
        for servico, dados in resumo.items():
            texto += f"- {servico}: {dados['quantidade']} vezes\n"

    # Exibir no campo de relatório
    campo_relatorio.delete('1.0', 'end')
    campo_relatorio.insert('1.0', texto)

    return atendimentos
    relatorio = gerar_relatorio_servicos(data_i, data_f)
    for atendimento in relatorio:
        print(atendimento.data_servico, atendimento.horario_servico)

    # Exportação para PDF e Excel
    linhas_pdf = texto.strip().split("\n")
    gerar_relatorio_pdf(linhas_pdf, nome_arquivo="servicos.pdf")

    linhas_excel = [["Serviço", "Quantidade"]] + [[s, d["quantidade"]] for s, d in resumo.items()]
    gerar_excel(linhas_excel, nome_arquivo="servicos.xlsx")

    tocar_faixa_relatorio()



def criar_frame_financeiro(inner_frame):
    frame_datas = ttk.LabelFrame(inner_frame, text="Relatórios Financeiros")
    frame_datas.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky="nsew")
    ttk.Label(frame_datas, text="Data Inicial:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    ttk.Label(frame_datas, text="Data Final:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    calendario_inicio = DateEntry(frame_datas, locale="pt_BR")
    calendario_inicio.grid(row=0, column=1, padx=5, pady=5)
    calendario_fim = DateEntry(frame_datas, locale="pt_BR")
    calendario_fim.grid(row=0, column=3, padx=5, pady=5)
    ttk.Button(frame_datas, text="Gerar Relatório Financeiro",
               command=lambda: gerar_relatorio_financeiro(calendario_inicio.get_date(), calendario_fim.get_date())
               ).grid(row=1, column=1, columnspan=2, padx=5)


def gerar_relatorio_financeiro(data_i, data_f):
    pagamentos = database.query(Pagamento).filter(
        Pagamento.data_pagamento >= data_i,
        Pagamento.data_pagamento <= data_f
    ).all()

    resumo = defaultdict(lambda: {"total": 0, "quantidade": 0})
    em_aberto = []

    for p in pagamentos:
        forma = p.forma_pagamento
        resumo[forma]["total"] += p.valor
        resumo[forma]["quantidade"] += 1
        if p.status_pagamento.lower() == "em aberto":
            em_aberto.append(p)

    texto = f"📊 Relatório Financeiro\n🗓️ De: {data_i} até {data_f}\n\n"
    for forma, dados in resumo.items():
        texto += f"- {forma}: {dados['quantidade']} pagamentos | Total: R${dados['total']:.2f}\n"

    if em_aberto:
        texto += "\n⚠️ Pagamentos em aberto:\n"
        for p in em_aberto:
            texto += f"  • {p.cliente.nome} | {p.servico} | R${p.valor:.2f} | {p.data_pagamento.strftime('%d/%m/%Y')}\n"

    campo_relatorio.delete('1.0', 'end')
    campo_relatorio.insert('1.0', texto)

    # Nome dinâmico do arquivo
    categorias = combobox_categorias.get()  # exemplo: "Financeiro"
    data_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    nome_pdf = f"{categorias}_{data_str}.pdf"
    nome_excel = f"{categorias}_{data_str}.xlsx"

    # Exportação
    linhas_pdf = texto.strip().split("\n")
    gerar_relatorio_pdf(linhas_pdf, nome_arquivo=nome_pdf)

    linhas_excel = [["Forma", "Quantidade", "Total"]] + [[f, d["quantidade"], d["total"]] for f, d in
                                                             resumo.items()]
    gerar_excel(linhas_excel, nome_arquivo=nome_excel)


# def gerar_relatorio():
#     categoria = combobox_categorias.get()
#     subcategoria = combobox_subcategoria.get()
#     data_i = calendario_inicio.get_date()
#     data_f = calendario_fim.get_date()
#
#     if categoria == "Financeiro":
#         gerar_relatorio_financeiro(data_i, data_f)
#     elif categoria == "Serviços":
#         gerar_relatorio_servicos(data_i, data_f)
#     elif categoria == "Cadastro":
#         gerar_relatorio_clientes(data_i, data_f)
#
#     # Salvar relatório em PDF com nome dinâmico
#     texto = campo_relatorio.get("1.0", "end").strip()
#     salvar_relatorio_pdf(texto, f"{categoria}_{subcategoria}")
#
# # Cria o frame principal de relatórios
#     frame = ttk.LabelFrame(inner_frame, text="Relatórios")
#     frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
#
#     tocar_som_relatorio()

def gerar_relatorio():
    data_i = calendario_inicial.get_date()
    data_f = calendario_final.get_date()
    categoria = combobox_categorias.get() if combobox_categorias else "Relatorio"
    subcategoria = combobox_subcategoria.get() if combobox_subcategoria else ""




    if categoria == "Financeiro":
        gerar_relatorio_financeiro(data_i, data_f)
    elif categoria == "Serviços":
        gerar_relatorio_servicos(data_i, data_f)
    elif categoria == "Cadastro":
        gerar_relatorio_clientes(data_i, data_f)
    elif categoria == "Pagamentos":
        gerar_relatorio_pagamentos(data_i, data_f)
    elif categoria == "Comparativos":
        gerar_relatorio_comparativos(data_i, data_f)
    else:
        # Relatório genérico
        resultados = database.query(Pagamento).filter(
            Pagamento.data_pagamento >= data_i,
            Pagamento.data_pagamento <= data_f
        ).all()
        texto = f"📄 Relatório Geral\n🗓️ De: {data_i} até {data_f}\n\n"
        for r in resultados:
            texto += f"- {r.cliente.nome} | R${r.valor:.2f} | {r.forma_pagamento}\n"
        campo_relatorio.delete('1.0', 'end')
        campo_relatorio.insert('1.0', texto)

    # Exportação automática para PDF
    texto = campo_relatorio.get("1.0", "end").strip()
    if texto:
        # data_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
        # nome_pdf = f"{categoria}_{subcategoria if subcategoria else ''}_{data_str}.pdf"
        salvar_relatorio(texto, categoria, subcategoria)

    # Som de confirmação
    tocar_som_relatorio()
    # Mascote
    mascote_imagem()


        #salvar_relatorio_pdf(texto, f"{categoria}_{subcategoria if subcategoria else ''}")

def gerar_relatorio_clientes(data_i, data_f):
    texto = f"👤 Relatório de Clientes\n🗓️ De: {data_i} até {data_f}\n\n"
    campo_relatorio.delete("1.0", "end")
    campo_relatorio.insert("1.0", texto)
    salvar_relatorio_pdf(texto, "Clientes")

def gerar_relatorio_pagamentos(data_i, data_f):
    texto = f"💳 Relatório de Pagamentos\n🗓️ De: {data_i} até {data_f}\n\n"
    campo_relatorio.delete("1.0", "end")
    campo_relatorio.insert("1.0", texto)
    salvar_relatorio_pdf(texto, "Pagamentos")

def gerar_relatorio_comparativos(data_i, data_f):
    texto = f"📊 Relatório Comparativo\n🗓️ De: {data_i} até {data_f}\n\n"
    campo_relatorio.delete("1.0", "end")
    campo_relatorio.insert("1.0", texto)
    salvar_relatorio_pdf(texto, "Comparativos")





#     def mascote_imagem(frame_pai):
#         caminho_img = os.path.join("imagensipojucao", "imagensipojucao", "mascote", "mascote.png",
#                                    "mascote_relatorio.png")
#         if os.path.exists(caminho_img):
#             img = Image.open(caminho_img).resize((120, 120))
#             img_tk = ImageTk.PhotoImage(img)
#             mascote = tk.Label(frame_pai, image=img_tk)
#             mascote.image = img_tk
#             mascote.grid(row=2, column=2, padx=10, pady=10, sticky="e")
#
# def mascote_imagem(frame_pai):
#     caminho_img = os.path.join("imagensipojucao", "imagensipojucao", "mascote", "mascote.png",
#                                    "mascote_relatorio.png")
#     if os.path.exists(caminho_img):
#         img = Image.open(caminho_img).resize((120, 120))
#         img_tk = ImageTk.PhotoImage(img)
#         mascote = tk.Label(frame_pai, image=img_tk)
#         mascote.image = img_tk
#         mascote.grid(row=2, column=2, padx=10, pady=10, sticky="e")
#

def tocar_som_relatorio():
    caminho_som = caminho_arquivo("breaking_news_intro_378273.mp3", subpasta="sons")
    if os.path.exists(caminho_som):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(caminho_som)
        pygame.mixer.music.play()

        # pygame.mixer.Sound(caminho_som).play()
    else:
        print("⚠️ Arquivo de som não encontrado:", caminho_som)


# def tocar_faixa_relatorio():
#     caminho_som = caminho_arquivo("soft_edit_tune.mp3", subpasta="sons")
#     if os.path.exists(caminho_som):
#         pygame.mixer.init()
#         pygame.mixer.music.load(caminho_som)
#         pygame.mixer.music.play()
#     else:
#         print("⚠️ Arquivo de música não encontrado:", caminho_som)

def tocar_faixa_relatorio():
    caminho_som = caminho_arquivo("soft_edit_tune.mp3", subpasta="sons")
    if os.path.exists(caminho_som):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(caminho_som)
        pygame.mixer.music.play()
    else:
        print("⚠️ Arquivo de música não encontrado:", caminho_som)

def mascote_imagem():
    caminho_img = os.path.join("imagensipojucao", "mascote_relatorio.png")
    if os.path.exists(caminho_img):
        img = Image.open(caminho_img).resize((350, 350))
        img_tk = ImageTk.PhotoImage(img)
        mascote = tk.Label(frame_relatorio, image=img_tk)
        mascote.image = img_tk
        mascote.grid(row=0, column=2, padx=20, pady=10, sticky="n")
    else:
        print("⚠️ Arquivo de imagem não encontrado:", caminho_img)

# === Função auxiliar para salvar relatório com nome dinâmico ===
def salvar_relatorio(texto, categoria, subcategoria=""):
    data_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    nome_pdf = f"{categoria}_{subcategoria}_{data_str}.pdf"
    salvar_relatorio_pdf(texto, nome_pdf)

    # Som de confirmação
    #tocar_som_relatorio()

    # Notificação automática (opcional)
    # notificar_admins()


    #def tocar_som_relatorio():
    # código para tocar faixa .mp3

    #def tocar_faixa_relatorio():
    # código para tocar outra faixa

    #def mascote_imagem(frame_pai):
    # código para exibir mascote

























































# #from dados_compartilhados import var_raca, caracteristicas_racas
# import tkinter as tk
# from tkinter import ttk
#
# #from aba_som import som_evento
# #from main import aba_relatórios, inner_frame
# import matplotlib.pyplot as plt
# from aba_som import tocar_som, alternar_som_estado
# from dados_compartilhados import variaveis
# import pygame
# pygame.mixer.init()
# import dados_compartilhados as dc
# #info = dc.caracteristicas_racas.get(dc.variaveis["var_raca"].get(), {})
# #som_evento("relatorio")
#
# from aba_som import som_relatorio
# som_relatorio() # ✅ Isso funciona!
#
#
# from utils_mensagens import (gerar_msg_servico, gerar_msg_pix, gerar_msg_explicativa, gerar_msg_admin)
# def enviar_tudo(cliente, texto_relatorio, pix_link):
#     enviar_relatorio_para_cliente(cliente, texto_relatorio, pix_link)
#     enviar_relatorio_para_administradores(texto_relatorio)
#
#     # Botão para enviar somente ao cliente
#     ttk.Button(frame_relatorio, text="Enviar para Cliente",
#                command=lambda: enviar_relatorio_para_cliente(cliente, texto_relatorio, pix_link)).grid(row=13, column=0,
#                                                                                                        padx=10, pady=10)
#
#     # Botão para enviar somente aos administradores
#     ttk.Button(frame_relatorio, text="Notificar Administradores",
#                command=lambda: enviar_relatorio_para_administradores(texto_relatorio)).grid(row=13, column=1, padx=10,
#                                                                                             pady=10)
#
#     # Botão para enviar tudo de uma vez
#     ttk.Button(frame_relatorio, text="Enviar Tudo",
#                command=lambda: enviar_tudo(cliente, texto_relatorio, pix_link)).grid(row=13, column=2, padx=10, pady=10)
#
#     label_status = ttk.Label(frame_relatorio, text="")
#     label_status.grid(row=14, column=0, columnspan=3)
#
#     def enviar_tudo(cliente, texto_relatorio, pix_link, janela):
#         # Aqui entraria a lógica de envio por e-mail ou sistema
#         print(f"Enviando para: {cliente}\nTexto: {texto_relatorio}\nPix: {pix_link}")
#
#         label_status.config(text="✅ Relatório enviado com sucesso!")
#         mostrar_mascote_expressivo(janela, "positivo")
#
# import dados_compartilhados as dc  # Importe o que precisar de forma compartilhada
#
#
# from mensageiro import enviar_mensagem_cliente, enviar_relatorio_administrador
#
#
#
#
#
#
#
#
# # 📈 Etapa 4: Tipos de relatórios gerenciais escaláveis
# #Você pode montar funções para cada uma dessas visões:
#
# def gerar_relatorio():
#     global calendario_inicial, calendario_final
#     data_inicial = calendario_inicial.get_date()
#     data_final = calendario_final.get_date()
#
#     # Checar cada combobox
#     if combobox_item and combobox_item.get():
#         item_selecionado = combobox_item.get()
#         ocorrencias = item['Relatórios']['Serviços']
#     elif combobox_item1 and combobox_item1.get():
#         item_selecionado = combobox_item1.get()
#         ocorrencias = item1['Relatórios']['Cadastro']
#     elif combobox_item2 and combobox_item2.get():
#         item_selecionado = combobox_item2.get()
#         ocorrencias = item2['Relatórios']['Pagamentos']
#     else:
#         campo_relatorio.delete('1.0', 'end')
#         campo_relatorio.insert('1.0', "⚠️ Por favor, selecione um item para pesquisa!")
#         return
#
#     # Monta e exibe texto
#     relatorio_texto = f"📄 Relatório do item {item_selecionado}\n"
#     relatorio_texto += f"🗓️ Data inicial: {data_inicial}\n"
#     relatorio_texto += f"🗓️ Data final: {data_final}\n"
#     relatorio_texto += f"📝 Ocorrências simuladas:\n- " + '\n- '.join(ocorrencias)
#
#     campo_relatorio.delete('1.0', 'end')
#     campo_relatorio.insert('1.0', relatorio_texto)
#
#
# # Implantando  ADMINISTRADORES Recebem Relatórios Completos
#
#
# lista_administradores = [
#     {"nome": "RAPHAEL", "telefone": "5511989078611"},
#     {"nome": "LINDINALVA", "telefone": "5511963174904"},
#     {"nome": "MARLENE", "telefone": "5511963405229"},
#     {"nome": "REINALDO", "telefone": "5511981772847"}
# ]
#
# admin_lista = [
#     {"nome": "RAPHAEL", "telefone": "5511989078611"},
#     {"nome": "LINDINALVA", "telefone": "5511963174904"},
#     {"nome": "MARLENE", "telefone": "5511963405229"},
#     {"nome": "REINALDO", "telefone": "5511981772847"}
# ]
#
# checkbox_vars = {}
#
# # frame_admins = ttk.LabelFrame(janela, text="Administradores para notificação")
# # frame_admins.place(x=20, y=60)
#
# def aba_relatorios(container):
#     frame_admins = ttk.LabelFrame(container, text="Administradores para notificação")
#     frame_admins.grid(row=0, column=0, padx=10, pady=10)
#
#     for i, admin in enumerate(admin_lista):
#         var = tk.BooleanVar()
#         checkbox_vars[admin["telefone"]] = var
#         tk.Checkbutton(frame_admins, text=admin["nome"], variable=var).grid(row=i, column=0, sticky="w")
#
#     var_raca = dc.variaveis.get("var_raca")
#     if var_raca:
#         info = dc.caracteristicas_racas.get(var_raca.get(), {})
#         print(f"ℹ️ Info da raça: {info}")
#     else:
#         print("⚠️ Variável 'var_raca' ainda não foi inicializada.")
#
#
# def enviar_para_admins_selecionados(texto):
#     for telefone, var in checkbox_vars.items():
#         if var.get():
#             enviar_via_whatsapp(telefone, f"📋 Relatório:\n{texto}")
#
# def notificar_administradores(relatorio_texto):
#     for adm in lista_administradores:
#         numero = adm["telefone"]
#         mensagem = f"📋 Relatório do sistema para {adm['nome']}:\n{relatorio_texto}"
#         enviar_via_whatsapp(numero, mensagem)
#
# # def notificar_administradores(relatorio_texto):
# #     for adm in lista_administradores:
# #         enviar_via_whatsapp(adm["5511989078611"], f"📋 Relatório do sistema:\n{relatorio_texto}") # RAPHAEL
# #         enviar_via_whatsapp(adm["5511963174904"], f"📋 Relatório do sistema:\n{relatorio_texto}") # LINDINALVA
# #         enviar_via_whatsapp(adm["5511963405229"], f"📋 Relatório do sistema:\n{relatorio_texto}") # MARLENE
# #         enviar_via_whatsapp(adm["5511981772847"], f"📋 Relatório do sistema:\n{relatorio_texto}") # REINALDO
# #         enviar_via_whatsapp(adm["telefone"], f"📋 Relatório do sistema:\n{relatorio_texto}")
#
# def usar_dados_relat_base_no_porte():
#     porte = dc.var_porte.get()
#     preco_banho = dc.dados_pet.get(porte, {}).get("preços", {}).get("Banho", 0)
#     print(f"Banho para porte {porte} custa R$ {preco_banho}")
#
#
# def aba_relatorios(aba_relatorios, inner_frame):
#     # Permitir expansão
#     aba_relatorios.grid_rowconfigure(0, weight=1)
#     aba_relatorios.grid_columnconfigure(0, weight=1)
#
#     # Canvas + Scrollbar
#     canvas = tk.Canvas(aba)
#     scrollbar_y = ttk.Scrollbar(aba, orient="vertical", command=canvas.yview)
#     canvas.configure(yscrollcommand=scrollbar_y.set)
#
#     canvas.grid(row=0, column=0, sticky="nsew")
#     scrollbar_y.grid(row=0, column=1, sticky="ns")
#
#     # Frame rolável
#     inner_frame = ttk.Frame(canvas)
#     canvas.create_window((0, 0), window=inner_frame, anchor="nw")
#     from mascote import mostrar_mascote_expressivo
#
#     servicos, valores = coletar_servicos_selecionados()
#  33   enviar_mensagem_cliente(id_cliente, servicos, valores)
#
#     enviar_relatorio_administrador(texto_do_relatorio, lista_admins)
#
#     mostrar_mascote_expressivo(janela, expressao="positivo")  # Ou "relatorio"
#
#     mostrar_mascote_expressivo(janela, "anotando")
#
#     frame_exemplo = ttk.LabelFrame(inner_frame, text="Seção de Exemplo")
#     frame_exemplo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
#
#     frame_data_pagamento = ttk.LabelFrame(inner_frame, text="Data do Pagamento")
#     frame_data_pagamento.grid(row=9, column=1, padx=10, pady=10, sticky="w")
#
#     # combobox_item = ttk.LabelFrame(inner_frame, text="Item para Relatório")
#     combobox_item = ttk.Combobox(frame_relatorios, values=item["Relatórios"]["Serviços"])
#     combobox_item.grid(row=10, column=1, padx=10, pady=10, sticky="nsew")
#     combobox_item.bind("<<ComboboxSelected>>", lambda event: [atualizar_item(
#         event)])  # Atualiza raças e imagem ao selecionar porte])  # Atualiza raças e imagem ao selecionar porte
#
#     # combobox_item1 = ttk.LabelFrame(inner_frame, text="Item para Relatório")
#     combobox_item1 = ttk.Combobox(frame_relatorios, values=item1["Relatórios"]["Cadastro"])
#     combobox_item1.grid(row=11, column=2, padx=10, pady=10, sticky="nsew")
#     combobox_item1.bind("<<ComboboxSelected>>", lambda event: [atualizar_item1(
#         event), ])  # Atualiza raças e imagem ao selecionar porte])  # Atualiza raças e imagem ao selecionar porte
#
#     # combobox_item = ttk.LabelFrame(inner_frame, text="Item para Relatório")
#     combobox_item2 = ttk.Combobox(frame_relatorios, values=item2["Relatórios"]["Pagamentos"])
#     combobox_item2.grid(row=12, column=3, padx=10, pady=10, sticky="nsew")
#     combobox_item2.bind("<<ComboboxSelected>>", lambda event: [atualizar_item2(
#         event)])  # Atualiza raças e imagem ao selecionar porte])  # Atualiza raças e imagem ao selecionar porte
#
#
#
#     def ajustar_scroll(event):
#         canvas.configure(scrollregion=canvas.bbox("all"))
#     inner_frame.bind("<Configure>", ajustar_scroll)
#
#     # === A partir daqui, crie widgets dentro do inner_frame ===
#
#     # Exemplo básico
#
#     ttk.Label(frame_exemplo, text="Alguma informação importante").grid(row=0, column=0, sticky="w")
#
#     # Repita quantos blocos quiser (outros frames, grids, entradas, etc.)
#
#     # Se quiser ativar algo quando o porte mudar
#     dc.var_porte.trace_add("write", lambda *args: atualizar_exemplo())
#
# def atualizar_exemplo():
#     porte = dc.var_porte.get()
#     print(f"Porte selecionado na aba é: {porte}")
#
# #Calendário Cadastrar Item
# def cadastrar_item():
#     data = calendario_cadastro.get_date()
#     print(f"Data cadastrada  {data}")  # Substitua por lógica de salvar o item
#     dc.label_resultado.config(text=f"Data cadastrada  {data}")
#
# # Configuração para expandir corretamente
# #aba_cadastro.columnconfigure(0, weight=1)
#
# # Frame para Data do Cadastro
#
# inner_frame = ttk.Frame(container)
# inner_frame.grid(row=1, column=0, padx=10, pady=10)
#
# frame_calendario_cadastro = ttk.LabelFrame(inner_frame, text="Calendario Cadastro")
# frame_calendario_cadastro.grid(row=0, column=0)
#
# calendario_cadastro = DateEntry(frame_calendario_cadastro, year=2025, locale='pt_br')
# calendario_cadastro.grid(row=0, column=0 , padx=10, pady=10, sticky='nsew')
#
# # Criando um Frame para Dados Cadastrais
# # frame_cadastramento = ttk.LabelFrame(aba_cadastro, text="Dados dos Cadastrais")
# # frame_cadastramento.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
#
# def criar_frame_cadastro(parent, text="Dados Cadastrais"):
#     frame_cadastro = ttk.LabelFrame(parent, )
#     frame_cadastro.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
#
#     frame_cadastro = ttk.Label(inner_frame, "Dados Cadastrais").grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
#
#     # nome Pet
#     ttk.Label(inner_frame, text="Nome do Pet", anchor='w').grid(row=1, column=0, padx=10, pady=5, sticky='ew')
#     entry_nome = tk.Entry(frame_cadastramento)
#     entry_nome.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
#
#     # idade
#     ttk.Label(inner_frame, text="Idade Anos").grid(row=2, column=0, padx=10, pady=10, sticky='w')
#     entry_idadedopetanos = ttk.Entry(inner_frame)
#     entry_idadedopetanos.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')
#
#     ttk.Label(inner_frame, text="Meses").grid(row=3, column=0, padx=10, pady=5, sticky='w')
#     entry_idadedopetmeses = ttk.Entry(inner_frame)
#     entry_idadedopetmeses.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
#
#     # Tutor 1
#     ttk.LabelFrame(inner_frame, text="Tutor 1").grid(row=4, column=0, padx=10, pady=10, sticky='w')
#     entry_tutor_1 = tk.Entry(inner_frame)
#     entry_tutor_1.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
#
#     # telefone1
#     ttk.Label(inner_frame, text="Telefone Tutor 1", anchor='e').grid(row=5, column=0, padx=10, pady=5, sticky='w')
#     entry_telefone_1 = tk.Entry(inner_frame)
#     entry_telefone_1.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
#     # email Tutor1
#     ttk.Label(inner_frame, text="email Tutor 1", anchor='e').grid(row=2, column=0, padx=10, pady=10, sticky='w')
#     entry_email_tutor_1 = tk.Entry(inner_frame)
#     entry_email_tutor_1.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
#
#     #tutor 2
#     # ttk.Label(aba_cadastro, text="Tutor 2", anchor='e').grid(row=3, column=0, padx=10, pady=5, sticky='ew')
#     # # Campo de entrada (Entry)
#     # entry_tutor_2 = tk.Entry(aba_cadastro)
#     # entry_tutor_2.grid(row=7, column=1, padx=10, pady=10, sticky='ew')
#
#     # Tutor 2
#     frame_tutor2 = ttk.LabelFrame(inner_frame, text="Tutor 2")
#     frame_tutor2.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
#
#     ttk.Label(frame_tutor2, text="Nome do Tutor").grid(row=0, column=0, padx=10, pady=5, sticky='w')
#     entry_tutor_2 = tk.Entry(frame_tutor2)
#     entry_tutor_2.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
#
#     #telefone 2
#     ttk.Label(frame_tutor2, text="Telefone Tutor 2", anchor='e').grid(row=1, column=1, padx=10, pady=5, sticky='ew')
#     # Campo de entrada (Entry)
#     entry_telefone_2 = tk.Entry(inner_frame)
#     entry_telefone_2.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
#     frame_telefone_2a = ttk.LabelFrame(inner_frame, text="Telefone_a", borderwidth=1, relief='solid')
#     entry_telefone_2a = tk.Entry(inner_frame)
#     entry_telefone_2a.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
#
#     #email Tutor2
#     frame_email_tutor_2 = ttk.LabelFrame(inner_frame, text="email Tutor 2", anchor='w')
#     frame_email_tutor_2.grid(row=2, column=0, padx=10, pady=5, sticky='ew')
#     entry_email_tutor_2 = tk.Entry(inner_frame)
#     entry_email_tutor_2.grid(row=10, column=0, padx=10, pady=10, sticky='nsew')
#
#     # Criando um Frame para Endereço e Observações
#     ttk.Label(inner_frame, text="Endereço e Observações").grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="nsew")
#     #logradouro.config(height=170)  # Define a altura manualmente
#
#     #frame_logradouro.grid_propagate(False)  # Impede que os widgets internos alterem o tamanho do frame
#
#
#     #Endereço Logradouro
#     ttk.Label(inner_frame, text="Endereço").grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
#     # Campo de entrada (Entry)
#     entry_enderecopet = tk.Entry(inner_frame)
#     entry_enderecopet.grid(row=2, column=1, padx=10, pady=10, sticky='nsew', columnspan=2)
#     #entry_nome.grid(row=1, column=0, columnspan=4, pady=1, sticky='nsew')
#
#     #endereço Número
#     frame_endereconumero = ttk.Label(inner_frame, text="Número", anchor='e')
#     frame_endereconumero.grid(row=3, column=1, padx=10, pady=10, sticky='nsew')
#     # Campo de entrada (Entry)
#     entry_endereconumero = tk.Entry(inner_frame)
#     entry_endereconumero.grid(row=3, column=2, padx=10, pady=10, sticky='nsew')
#
#     #Endereço Complemento
#     frame_enderecocomplemento = ttk.Label(inner_frame, text="Complemento", anchor='e')
#     frame_enderecocomplemento.grid(row=4, column=1, padx=10, pady=10, sticky='nsew')
#     # Campo de entrada (Entry)
#     entry_enderecocomplemento = tk.Entry(inner_frame)
#     entry_enderecocomplemento.grid(row=4, column=2, padx=10, pady=10, sticky='nsew')
#
#
#
#     # frame_recomendacoes = ttk.Label(aba_cadastro, text="Recomendações", borderwidth=1, relief='solid')
#     # frame_recomendacoes.grid(row=20, column=0, columnspan=2, padx=10, pady=5, sticky="w")
#     #
#     # # Observações sobre o PET
#     # frame_recomendacoes = ttk.Label(aba_cadastro, text="Recomendações Sobre o pet", borderwidth=1, relief='solid' )
#     # frame_recomendacoes.grid(row=21, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
#     # Campo de entrada (Entry)\\
#     campo_observacoes = tk.Text(inner_frame, width=80, height=12, borderwidth=2, relief='solid' )
#     campo_observacoes.grid(row=30, column=0, columnspan=2, padx=10, pady=10)
#
#     # Configuração para expandir corretamente
#     janela.columnconfigure(0, weight=1)
#     janela.rowconfigure(0, weight=1)
#     aba_cadastro.columnconfigure(1, weight=1)
# #=
#
# # entry_recomendacoes = tk.Entry(frame_recomendacoes)
# # entry_recomendacoes.grid(row=0, column=3, padx=10, pady=10, sticky='nsew', columnspan=3)
#
# # #Criando um Frame para Endereço e Observações
# # frame_recomendacoes = ttk.LabelFrame(inner_frame, text="Recomendações Sobre o PET")
# # frame_cadastro.grid(row=2, column=5, columnspan=6, padx=10, pady=5, sticky="nsew")
# # dc.label_relatorio = tk.Label(frame_relatorio, text="Recomendações", borderwidth=1, relief='solid' )
# # #Campo para exibir o relatório
# # campo_observacoes = tk.Text(frame_cadastro, width=50, height=10, borderwidth=2, relief='solid' )
# # campo_observacoes.grid(row=4, column=0, columnspan=4, padx=10, pady=10)
#
#
# #RELATÓRIOS:
#
# # Definindo variáveis globais
# combobox_item = None
# combobox_item1 = None
# combobox_item2 = None
# calendario_inicial = None
# calendario_final = None
#
#
# item= {
#     "Relatórios": {
#         "Serviços": ['Banho', 'Hidratação', 'Desembolo', 'Remoção Pelos', 'Corte Unhas', 'Escovação Dentes', 'Tosa Higiênica', 'Tosa Máquina', 'Tosa Tesoura', 'Leva Trás']}}
#                   #
#
# item1= {
#     "Relatórios": {
#         "Cadastro": ['Cadastrado Desde', 'Nome Pet', 'Idade', 'Tutor 1', 'Tutor 2', 'Telefone Tutor 1', 'email Tutor 1',
#                   'Telefone Tutor 2', 'email Tutor 2', 'Endereço', 'Número', 'Complemento', 'Recomendações']}}
#
# item2= {
#     "Relatórios": {
#         "Pagamentos": ['Condições Pagamento', 'Abatimentos', 'Status Pagamento', 'Data Pagamento', 'Forma Pagamento']}}
#
#
#
#
#
#
# # Frame para combobox item
#
# # combobox_porte = ttk.Combobox(inner_frame, values=list(dados_pet.keys()))
# # combobox_porte.grid(row=0, column=0, padx=10, pady=5)
# #combobox_porte.bind("<<ComboboxSelected>>", atualizar_lista_racas)  # Atualiza raças ao selecionar porte
#
#
# #scrollable_frame.rowconfigure(0, weight=1)  # Para o row 0 (combobox)
#
#
# # combobox_item = ttk.LabelFrame(inner_frame, text="Calendario Cadastro")
# # combobox_item = ttk.Combobox(inner_frame, values=list(dados_pet.keys()))
# # combobox_item.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")
# # scrollable_frame.rowconfigure(0, weight=1)  # Para o row 0 (combobox)
#
#
#
# # Função única para gerar relatórios
# def gerar_relatorio(event=None):
#     global calendario_inicial, calendario_final
#
#
#     # Captura das datas e do item selecionado
#     date_inicial = calendario_inicial.get_date()
#     data_final = calendario_final.get_date()
#     item_selecionado = None # Definido à seguir
#
#     # Verifica qual combobox está sendo utilizado
#     if combobox_item.get():
#         item_selecionado = combobox_item.get()
#         relatorio_texto = f"Relatório do item {item_selecionado}\nOcorrências simuladas: {item['Relatórios']['Serviços']}"
#     elif combobox_item1.get():
#         item_selecionado = combobox_item1.get()
#         relatorio_texto = f"Relatório do item {item_selecionado}\nOcorrências simuladas: {item1['Relatórios']['Cadastro']}"
#     elif combobox_item2.get():
#         item_selecionado = combobox_item2.get()
#         relatorio_texto = f"Relatório do item {item_selecionado}\nOcorrências simuladas:{item2['Relatórios']['Pagamentos']}"
#     else:
#         relatotio_texto = "Por favor, selecione um item para pesquisa!"
#
#         # Exibir o relatório no campo de texto
#     campo_relatorio.delete('1.0', 'end')
#     campo_relatorio.insert('1.0', relatorio_texto)
#
# # Configuraçao dos Calendário
# #
# #
# #
# #
# #
# #
# #
# #
# #     combobox_item = ttk.Combobox(scrollable_frame, values=list(dados_pet.keys()))
# #     combobox_item.grid(row=1, column=2, padx=10, pady=5)
# #     #combobox_porte.bind("<<ComboboxSelected>>", atualizar_lista_racas)  # Atualiza raças ao selecionar porte
# #     combobox_item.bind("<<ComboboxSelected>>", lambda event: [atualizar_lista_racas(event), update_porte_image(event)])  # Atualiza raças e imagem ao selecionar porte
# #     scrollable_frame.rowconfigure(0, weight=1)  # Para o row 0 (combobox)
# #
# def gerar_relatorio():
#     # Capturar as datas e o item selecionado
#     global calendario_inicial, calendario_final, combobox_item
#
#     data_inicial = calendario_inicial.get_date()
#     data_final = calendario_final.get_date()
#     item_selecionado = combobox_item.get()
#
#
#     # Verificar se o item foi selecionado e as datas estão corretas
#     if not item_selecionado:
#         relatorio_texto = "Por favor, selecione um item para a pesquisa!\n"
#     elif not data_inicial or not data_final:
#         relatorio_texto = "Por favor, selecione a datas inicial e final!\n"
#     else:
#         # Criar o texto do relatório
#         relatorio_texto = f"Relatório do item  {item_selecionado}\n"
#         relatorio_texto += f"Data inicial  {data_inicial}\n"
#         relatorio_texto += f"Data final  {data_final}\n"
#         relatorio_texto += f"Ocorrências simuladas: ['Banho', 'Hidratação', 'Desembolo', 'Remoção Pelos', 'Corte Unhas', 'Escovação Dentes', 'Tosa Higiênica', 'Tosa Máquina', 'Tosa Tesoura', 'Leva Trás']"
#
# def gerar_relatorio():
#     # Capturar as datas e o item selecionado
#     global calendario_inicial, calendario_final, combobox_item1
#
#     data_inicial = calendario_inicial.get_date()
#     data_final = calendario_final.get_date()
#     item_selecionado = combobox_item1.get()
#
#
#     # Verificar se o item foi selecionado e as datas estão corretas
#     if not item_selecionado:
#         relatorio_texto = "Por favor, selecione um item para a pesquisa!\n"
#     elif not data_inicial or not data_final:
#         relatorio_texto = "Por favor, selecione a datas inicial e final!\n"
#     else:
#         # Criar o texto do relatório
#         relatorio_texto = f"Relatório do item  {item_selecionado}\n"
#         relatorio_texto += f"Data inicial  {data_inicial}\n"
#         relatorio_texto += f"Data final  {data_final}\n"
#         relatorio_texto += f"Ocorrências simuladas: ['Cadastrado Desde', 'Nome Pet', 'Idade', 'Tutor 1', 'Tutor 2', 'Telefone Tutor 1', 'email Tutor 1',                 'Telefone Tutor 2', 'email Tutor 2', 'Endereço', 'Número', 'Complemento', 'Recomendações']"
#
#
#
# def gerar_relatorio():
#     # Capturar as datas e o item selecionado
#     global calendario_inicial, calendario_final, combobox_item2
#
#     data_inicial = calendario_inicial.get_date()
#     data_final = calendario_final.get_date()
#     item_selecionado = combobox_item2.get()
#
#
#     # Verificar se o item foi selecionado e as datas estão corretas
#     if not item_selecionado:
#         relatorio_texto = "Por favor, selecione um item para a pesquisa!\n"
#     elif not data_inicial or not data_final:
#         relatorio_texto = "Por favor, selecione a datas inicial e final!\n"
#     else:
#         # Criar o texto do relatório
#         relatorio_texto = f"Relatório do item  {item_selecionado}\n"
#         relatorio_texto += f"Data inicial  {data_inicial}\n"
#         relatorio_texto += f"Data final  {data_final}\n"
#         relatorio_texto += f"Ocorrências simuladas: ['Condições Pagamento', 'Abatimentos', 'Status Pagamento', 'Data Pagamento', 'Forma Pagamento']"
#
#
#
# def update_porte_item1(event=None):
#     global combobox_item1
#     porte = combobox_item1.get().strip()
#
# def gerar_relatorio():
#     # Capturar as datas e o item selecionado
#     global calendario_inicial, calendario_final, combobox_item
#
#     data_inicial = calendario_inicial.get_date()
#     data_final = calendario_final.get_date()
#     item_selecionado = combobox_item.get()
#
#
#     # Verificar se o item foi selecionado e as datas estão corretas
#     if not item_selecionado:
#         relatorio_texto = "Por favor, selecione um item para a pesquisa!\n"
#     elif not data_inicial or not data_final:
#         relatorio_texto = "Por favor, selecione a datas inicial e final!\n"
#     else:
#         # Criar o texto do relatório
#         relatorio_texto = f"Relatório do item  {item_selecionado}\n"
#         relatorio_texto += f"Data inicial  {data_inicial}\n"
#         relatorio_texto += f"Data final  {data_final}\n"
#         relatorio_texto += f"Ocorrências simuladas: ['Porte', 'Raça', 'Serviço', 'Condições Pagamento', 'Abatimentos', 'Status Pagamento', 'Data Pagamento', 'Forma Pagamento', 'Cadastrado Desde', 'Nome Pet', 'Idade', 'Tutor 1', 'Tutor 2', 'Telefone 1', 'Telefone 2', 'Endereço', 'Poodle', 'Recomendações', 'Em Aberto-Total', 'Pago-Total', 'Em Aberto-Individual', 'Pago-Individual']"
#
#         # Exibir o relatório no campo de texto
#     campo_relatorio.delete('1.0', 'end')
#     campo_relatorio.insert('1.0', relatorio_texto)
#
# # Configuração de Calendários
# frame_calendario_inicial = ttk.LabelFrame(inner_frame, text="Data Inicial-Relatório")
# frame_calendario_inicial.grid(row=2, column=3, padx=10, pady=10, sticky="w")
# date_inicial = DateEntry(inner_frame, year=2025, locale='pt_br')
# date_inicial.grid(row=3, column=3 , padx=10, pady=10, sticky='nsew')
#
# frame_calendario_final = ttk.LabelFrame(inner_frame, text="Data Final-Relatório")
# frame_calendario_final.grid(row=2, column=4, padx=10, pady=10, sticky="w")
# date_final = DateEntry(inner_frame, year=2025, locale='pt_br')
# date_final.grid(row=3, column=5 , padx=10, pady=10, sticky='nsew')
#
# def limpar_relatorio():
#     campo_relatorio.delete('1.0', 'end')
#
# #Botão para limpar o relatório exibido
# botao_limpar = ttk.Button(inner_frame, text="Limpar Relatório", command=limpar_relatorio)
# botao_limpar.grid(row=5, column=4, pady=6)
#
#
# # Criando um Frame para Relatório
# frame_relatorio = ttk.LabelFrame(inner_frame, text="Relatórios-(Cadastro, Serviços, Controle Pagamentos)")
# frame_relatorio.grid(row=3, column=5, columnspan=2, padx=10, pady=5, sticky="w")
# dc.label_relatorio = tk.Label(frame_relatorio, text="Recomendações", borderwidth=1, relief='solid' )
#
# # Campo para exibir o relatório
# campo_relatorio = tk.Text(frame_relatorio, width=50, height=5, borderwidth=2, relief='solid')
# campo_relatorio.grid(row=4, column=5, columnspan=2, padx=10, pady=10)
#
#
#
# # Botão para gerar relatório
# botao_gerar = ttk.Button(aba_relatórios, text="Gerar Relatório", command=gerar_relatorio)
# botao_gerar.grid(row=3, column=4, pady=6)
# #
# # Botão para limpar o relatório exibido
# botao_limpar = ttk.Button(aba_relatórios, text="Limpar Relatório", command=limpar_relatorio)
# botao_limpar.grid(row=6, column=4, pady=6)
#
# botao_fechar = tk.Button(text='Fechar', command=janela.quit, borderwidth=2, relief='solid')
# botao_fechar.grid(row=3, column=6, padx=6, pady=10, sticky='nsew', columnspan=4)
